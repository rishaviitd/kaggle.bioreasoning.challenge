"""
Build a unique mouse gene enrichment dictionary.

The output JSON maps each unique gene symbol from train/test CSV files to:
  - info: mygene.info annotations
  - interaction: STRING DB protein interaction partners

The script is resumable: if the output JSON already exists, completed genes are
skipped unless --force is passed.
"""

from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
import time
import urllib.parse
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_TRAIN_CSV = ROOT_DIR / "data/train.csv"
DEFAULT_TEST_CSV = ROOT_DIR / "data/test.csv"
DEFAULT_OUTPUT_JSON = ROOT_DIR / "data/enrichment/unique_gene_context.json"

MYGENE_URL = "https://mygene.info/v3/query"
STRING_URL = "https://string-db.org/api/json/interaction_partners"
MOUSE_TAXID = 10090


def load_unique_genes(train_csv: Path, test_csv: Path) -> list[str]:
    print(f"[load] Reading train CSV: {train_csv}")
    train_df = pd.read_csv(train_csv)
    print(f"[load] Reading test CSV:  {test_csv}")
    test_df = pd.read_csv(test_csv)

    required = {"pert", "gene"}
    for name, df in [("train", train_df), ("test", test_df)]:
        missing = required - set(df.columns)
        if missing:
            raise ValueError(f"{name} CSV is missing columns: {sorted(missing)}")

    genes = set(train_df["pert"].dropna().astype(str).str.strip())
    genes.update(train_df["gene"].dropna().astype(str).str.strip())
    genes.update(test_df["pert"].dropna().astype(str).str.strip())
    genes.update(test_df["gene"].dropna().astype(str).str.strip())
    genes.discard("")

    sorted_genes = sorted(genes)
    print(f"[load] Unique genes found across train/test: {len(sorted_genes)}")
    return sorted_genes


def read_json_if_exists(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    print(f"[resume] Loading existing enrichment cache: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, dict):
        raise ValueError(f"Expected object at {path}, got {type(data).__name__}")
    print(f"[resume] Existing cached genes: {len(data)}")
    return data


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = path.with_suffix(path.suffix + ".tmp")
    with tmp_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True)
        f.write("\n")
    tmp_path.replace(path)


def request_json(url: str, params: dict[str, str], timeout: int) -> Any:
    query = urllib.parse.urlencode(params)
    req = urllib.request.Request(f"{url}?{query}")
    req.add_header("Accept", "application/json")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    if isinstance(value, dict):
        return [value]
    return []


def dedupe_dicts_by_key(items: list[dict[str, Any]], key: str) -> list[dict[str, Any]]:
    seen: set[str] = set()
    out: list[dict[str, Any]] = []
    for item in items:
        value = item.get(key)
        if not value or value in seen:
            continue
        seen.add(value)
        out.append(item)
    return out


def compact_text(parts: list[str]) -> str:
    return "\n".join(part for part in parts if part)


def annotation_strength(info: dict[str, Any], interaction: dict[str, Any]) -> str:
    score = 0
    if info.get("summary"):
        score += 2
    if info.get("go_bp_terms"):
        score += 1
    if info.get("kegg_pathways"):
        score += 1
    if interaction.get("partners"):
        score += 1

    if score >= 4:
        return "strong"
    if score >= 2:
        return "medium"
    return "weak"


def is_uncharacterized(name: str | None, summary: str | None, go_terms: list[str]) -> bool:
    text = " ".join([name or "", summary or "", " ".join(go_terms)]).lower()
    weak_names = ["riken cdna", "predicted gene", "uncharacterized", "biological_process"]
    if any(marker in text for marker in weak_names):
        return True
    return not summary and not go_terms


def fetch_gene_info(gene_symbol: str, timeout: int) -> dict[str, Any]:
    try:
        data = request_json(
            MYGENE_URL,
            {
                "q": f"symbol:{gene_symbol}",
                "species": "mouse",
                "fields": "symbol,name,summary,go.BP,pathway.kegg,taxid,entrezgene",
                "size": "1",
            },
            timeout,
        )
    except Exception as exc:
        return {
            "status": "error",
            "source": "mygene.info",
            "query_symbol": gene_symbol,
            "error": str(exc),
        }

    hits = data.get("hits", []) if isinstance(data, dict) else []
    if not hits:
        return {
            "status": "not_found",
            "source": "mygene.info",
            "query_symbol": gene_symbol,
            "matched_symbol": None,
            "name": None,
            "summary": None,
            "go_bp_terms": [],
            "go_bp": [],
            "kegg_pathways": [],
            "kegg": [],
            "is_uncharacterized": True,
            "error": None,
        }

    hit = hits[0]
    go_bp_raw = as_list(hit.get("go", {}).get("BP") if isinstance(hit.get("go"), dict) else None)
    go_bp = []
    for term in dedupe_dicts_by_key(go_bp_raw, "term"):
        go_bp.append(
            {
                "id": term.get("id"),
                "term": term.get("term"),
                "evidence": term.get("evidence"),
                "qualifier": term.get("qualifier"),
            }
        )

    kegg_raw = as_list(
        hit.get("pathway", {}).get("kegg") if isinstance(hit.get("pathway"), dict) else None
    )
    kegg = []
    for pathway in dedupe_dicts_by_key(kegg_raw, "name"):
        kegg.append({"id": pathway.get("id"), "name": pathway.get("name")})

    go_terms = [item["term"] for item in go_bp if item.get("term")]
    kegg_names = [item["name"] for item in kegg if item.get("name")]
    name = hit.get("name")
    summary = hit.get("summary")
    matched_symbol = hit.get("symbol")

    raw_text = compact_text(
        [
            f"Gene: {matched_symbol or gene_symbol}",
            f"Full name: {name}" if name else "",
            f"Summary: {summary}" if summary else "",
            f"GO Biological Process: {'; '.join(go_terms)}" if go_terms else "",
            f"KEGG Pathways: {'; '.join(kegg_names)}" if kegg_names else "",
        ]
    )

    return {
        "status": "ok",
        "source": "mygene.info",
        "query_symbol": gene_symbol,
        "matched_symbol": matched_symbol,
        "taxid": hit.get("taxid"),
        "entrezgene": hit.get("entrezgene"),
        "name": name,
        "summary": summary,
        "go_bp_terms": go_terms,
        "go_bp": go_bp,
        "kegg_pathways": kegg_names,
        "kegg": kegg,
        "has_summary": bool(summary),
        "has_go": bool(go_terms),
        "has_kegg": bool(kegg_names),
        "is_uncharacterized": is_uncharacterized(name, summary, go_terms),
        "raw_text": raw_text,
        "error": None,
    }


def fetch_protein_interactions(gene_symbol: str, timeout: int) -> dict[str, Any]:
    try:
        data = request_json(
            STRING_URL,
            {
                "identifiers": gene_symbol,
                "species": str(MOUSE_TAXID),
            },
            timeout,
        )
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            return {
                "status": "not_found",
                "source": "STRING DB",
                "query_symbol": gene_symbol,
                "species": MOUSE_TAXID,
                "partners": [],
                "top_partner_symbols": [],
                "has_interactions": False,
                "raw_text": f"No protein interactions found for {gene_symbol} in mouse (STRING DB).",
                "error": None,
            }
        return {
            "status": "error",
            "source": "STRING DB",
            "query_symbol": gene_symbol,
            "species": MOUSE_TAXID,
            "partners": [],
            "top_partner_symbols": [],
            "error": str(exc),
        }
    except Exception as exc:
        return {
            "status": "error",
            "source": "STRING DB",
            "query_symbol": gene_symbol,
            "species": MOUSE_TAXID,
            "partners": [],
            "top_partner_symbols": [],
            "error": str(exc),
        }

    if not data:
        return {
            "status": "not_found",
            "source": "STRING DB",
            "query_symbol": gene_symbol,
            "species": MOUSE_TAXID,
            "partners": [],
            "top_partner_symbols": [],
            "has_interactions": False,
            "raw_text": f"No protein interactions found for {gene_symbol} in mouse (STRING DB).",
            "error": None,
        }

    partners = []
    for entry in data:
        partners.append(
            {
                "symbol": entry.get("preferredName_B"),
                "score": entry.get("score"),
                "string_id": entry.get("stringId_B"),
                "evidence_scores": {
                    "neighborhood": entry.get("nscore"),
                    "fusion": entry.get("fscore"),
                    "cooccurrence": entry.get("pscore"),
                    "coexpression": entry.get("ascore"),
                    "experimental": entry.get("escore"),
                    "database": entry.get("dscore"),
                    "textmining": entry.get("tscore"),
                },
            }
        )

    top_partner_symbols = [p["symbol"] for p in partners if p.get("symbol")]
    raw_text = compact_text(
        [
            f"Protein interactions for {gene_symbol} (mouse, STRING DB):",
            *[
                f"- {p['symbol']} (combined score: {p['score']:.3f})"
                for p in partners
                if p.get("symbol") and isinstance(p.get("score"), (int, float))
            ],
        ]
    )

    return {
        "status": "ok",
        "source": "STRING DB",
        "query_symbol": gene_symbol,
        "species": MOUSE_TAXID,
        "partners": partners,
        "top_partner_symbols": top_partner_symbols,
        "has_interactions": bool(partners),
        "raw_text": raw_text,
        "error": None,
    }


def enrich_gene(gene_symbol: str, args: argparse.Namespace) -> dict[str, Any]:
    info = fetch_gene_info(
        gene_symbol,
        timeout=args.timeout,
    )
    if args.sleep > 0:
        time.sleep(args.sleep)

    interaction = fetch_protein_interactions(
        gene_symbol,
        timeout=args.timeout,
    )
    strength = annotation_strength(info, interaction)
    info["annotation_strength"] = strength
    return {"info": info, "interaction": interaction}


def build_context(args: argparse.Namespace) -> None:
    genes = load_unique_genes(args.train_csv, args.test_csv)
    if args.limit:
        print(f"[config] Limiting run to first {args.limit} genes for testing.")
        genes = genes[: args.limit]

    context = {} if args.force else read_json_if_exists(args.output_json)
    print(f"[start] Enriching {len(genes)} genes.")
    print(f"[output] {args.output_json}")
    print(f"[config] Workers: {args.workers}")

    pending_genes = [gene for gene in genes if args.force or gene not in context]
    skipped = len(genes) - len(pending_genes)
    print(f"[resume] Genes skipped from cache: {skipped}")
    print(f"[queue] Genes queued for fetching: {len(pending_genes)}")

    completed = 0
    if not pending_genes:
        print("[done] Nothing to fetch.")
        write_json(args.output_json, context)
        return

    def fetch_one(gene_symbol: str) -> tuple[str, dict[str, Any]]:
        if args.sleep > 0:
            time.sleep(args.sleep)
        return gene_symbol, enrich_gene(gene_symbol, args)

    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        future_to_gene = {executor.submit(fetch_one, gene): gene for gene in pending_genes}
        for future in as_completed(future_to_gene):
            gene_symbol = future_to_gene[future]
            try:
                gene_symbol, enriched = future.result()
            except Exception as exc:
                print(f"[error] {gene_symbol}: {exc}")
                enriched = {
                    "info": {
                        "status": "error",
                        "source": "mygene.info",
                        "query_symbol": gene_symbol,
                        "error": str(exc),
                    },
                    "interaction": {
                        "status": "error",
                        "source": "STRING DB",
                        "query_symbol": gene_symbol,
                        "species": MOUSE_TAXID,
                        "partners": [],
                        "top_partner_symbols": [],
                        "error": str(exc),
                    },
                }

            context[gene_symbol] = enriched
            completed += 1
            total_done = skipped + completed
            print(f"[{total_done}/{len(genes)}] Done {gene_symbol}")

            if completed % args.save_every == 0:
                print(f"[save] Writing checkpoint after {completed} newly fetched genes.")
                write_json(args.output_json, context)

    print(f"[save] Writing final output. fetched={completed}, skipped={skipped}")
    write_json(args.output_json, context)
    print("[done] Gene enrichment dictionary is ready.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build unique gene enrichment dictionary.")
    parser.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN_CSV)
    parser.add_argument("--test-csv", type=Path, default=DEFAULT_TEST_CSV)
    parser.add_argument("--output-json", type=Path, default=DEFAULT_OUTPUT_JSON)
    parser.add_argument("--limit", type=int, default=None, help="Limit genes for a test run.")
    parser.add_argument("--force", action="store_true", help="Refetch genes already in output JSON.")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--sleep", type=float, default=0.15, help="Seconds to sleep between API calls.")
    parser.add_argument("--save-every", type=int, default=25)
    parser.add_argument("--workers", type=int, default=8, help="Parallel API request workers.")
    return parser.parse_args()


if __name__ == "__main__":
    build_context(parse_args())
