"""
Run EDA on gene enrichment features against train labels.

This script reads:
  - data/train.csv
  - data/enrichment/unique_gene_context.json

It writes:
  - data/enrichment/eda/enrichment_feature_eda_report.md
  - data/enrichment/eda/enrichment_feature_buckets.csv
  - data/enrichment/eda/enrichment_feature_rows.csv
  - data/enrichment/eda/enrichment_feature_ranked.csv
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]
DEFAULT_TRAIN_CSV = ROOT_DIR / "data/train.csv"
DEFAULT_CONTEXT_JSON = ROOT_DIR / "data/enrichment/unique_gene_context.json"
DEFAULT_OUTPUT_DIR = ROOT_DIR / "data/enrichment/eda"
LABELS = ["none", "up", "down"]
GENERIC_GO_TERMS = {"biological_process"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="EDA for enrichment features vs labels.")
    parser.add_argument("--train-csv", type=Path, default=DEFAULT_TRAIN_CSV)
    parser.add_argument("--context-json", type=Path, default=DEFAULT_CONTEXT_JSON)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT_DIR)
    return parser.parse_args()


def load_inputs(train_csv: Path, context_json: Path) -> tuple[pd.DataFrame, dict[str, Any]]:
    print(f"[load] Reading train labels: {train_csv}")
    train_df = pd.read_csv(train_csv)
    print(f"[load] Reading enrichment context: {context_json}")
    with context_json.open("r", encoding="utf-8") as f:
        context = json.load(f)

    required = {"pert", "gene", "label"}
    missing = required - set(train_df.columns)
    if missing:
        raise ValueError(f"Train CSV is missing columns: {sorted(missing)}")

    print(f"[load] Train rows: {len(train_df)}")
    print(f"[load] Cached genes: {len(context)}")
    print(f"[load] Unique train perturbations: {train_df['pert'].nunique()}")
    print(f"[load] Unique train target genes: {train_df['gene'].nunique()}")
    return train_df, context


def safe_info(context: dict[str, Any], symbol: str) -> dict[str, Any]:
    return (context.get(symbol) or {}).get("info") or {}


def safe_interaction(context: dict[str, Any], symbol: str) -> dict[str, Any]:
    return (context.get(symbol) or {}).get("interaction") or {}


def meaningful_go_terms(info: dict[str, Any]) -> set[str]:
    terms = info.get("go_bp_terms") or []
    return {
        str(term).strip().lower()
        for term in terms
        if str(term).strip() and str(term).strip().lower() not in GENERIC_GO_TERMS
    }


def kegg_terms(info: dict[str, Any]) -> set[str]:
    terms = info.get("kegg_pathways") or []
    return {str(term).strip().lower() for term in terms if str(term).strip()}


def partner_score(interaction: dict[str, Any], target_gene: str) -> float | None:
    target_lower = target_gene.lower()
    best_score: float | None = None
    for partner in interaction.get("partners") or []:
        symbol = str(partner.get("symbol") or "").lower()
        if symbol != target_lower:
            continue
        score = partner.get("score")
        if isinstance(score, int | float):
            best_score = max(best_score if best_score is not None else -1.0, float(score))
    return best_score


def short_strength(info: dict[str, Any]) -> str:
    if info.get("is_uncharacterized"):
        return "uncharacterized"
    return str(info.get("annotation_strength") or "missing")


def count_bin(value: int) -> str:
    if value == 0:
        return "0"
    if value <= 2:
        return "1-2"
    if value <= 5:
        return "3-5"
    if value <= 20:
        return "6-20"
    return "20+"


def jaccard_bin(value: float) -> str:
    if value == 0:
        return "0"
    if value <= 0.05:
        return "0-0.05"
    if value <= 0.10:
        return "0.05-0.10"
    if value <= 0.25:
        return "0.10-0.25"
    return "0.25+"


def string_score_bin(score: float | None) -> str:
    if score is None:
        return "not_found"
    if score < 0.4:
        return "0-0.4"
    if score < 0.7:
        return "0.4-0.7"
    if score < 0.9:
        return "0.7-0.9"
    return "0.9-1.0"


def closeness_level(score: int) -> str:
    if score == 0:
        return "low"
    if score <= 2:
        return "medium"
    return "high"


def build_feature_rows(train_df: pd.DataFrame, context: dict[str, Any]) -> pd.DataFrame:
    print("[features] Building row-level enrichment features...")
    rows: list[dict[str, Any]] = []

    for idx, row in train_df.iterrows():
        if idx and idx % 1000 == 0:
            print(f"[features] Processed {idx}/{len(train_df)} rows...")

        pert = str(row["pert"])
        gene = str(row["gene"])
        pert_info = safe_info(context, pert)
        gene_info = safe_info(context, gene)
        pert_inter = safe_interaction(context, pert)
        gene_inter = safe_interaction(context, gene)

        pert_go = meaningful_go_terms(pert_info)
        gene_go = meaningful_go_terms(gene_info)
        shared_go = pert_go & gene_go
        go_union = pert_go | gene_go

        pert_kegg = kegg_terms(pert_info)
        gene_kegg = kegg_terms(gene_info)
        shared_kegg = pert_kegg & gene_kegg

        score = partner_score(pert_inter, gene)
        target_in_string = score is not None
        target_strong = short_strength(gene_info) == "strong"
        closeness_score = int(bool(shared_go)) + int(bool(shared_kegg)) + (2 if target_in_string else 0)
        closeness_score += int(target_strong)

        rows.append(
            {
                "id": row.get("id", f"{pert}_{gene}"),
                "pert": pert,
                "gene": gene,
                "label": row["label"],
                "pert_cached": pert in context,
                "gene_cached": gene in context,
                "target_in_pert_string": target_in_string,
                "string_score": score,
                "string_score_bin": string_score_bin(score),
                "shared_go": bool(shared_go),
                "shared_go_count": len(shared_go),
                "go_jaccard": len(shared_go) / len(go_union) if go_union else 0.0,
                "go_jaccard_bin": jaccard_bin(len(shared_go) / len(go_union) if go_union else 0.0),
                "shared_kegg": bool(shared_kegg),
                "shared_kegg_count": len(shared_kegg),
                "pert_has_summary": bool(pert_info.get("summary")),
                "gene_has_summary": bool(gene_info.get("summary")),
                "pert_has_go": bool(pert_go),
                "gene_has_go": bool(gene_go),
                "pert_has_kegg": bool(pert_kegg),
                "gene_has_kegg": bool(gene_kegg),
                "pert_is_uncharacterized": bool(pert_info.get("is_uncharacterized")),
                "gene_is_uncharacterized": bool(gene_info.get("is_uncharacterized")),
                "pert_annotation_strength": short_strength(pert_info),
                "gene_annotation_strength": short_strength(gene_info),
                "pert_go_count": len(pert_go),
                "gene_go_count": len(gene_go),
                "pert_go_count_bin": count_bin(len(pert_go)),
                "gene_go_count_bin": count_bin(len(gene_go)),
                "pert_kegg_count": len(pert_kegg),
                "gene_kegg_count": len(gene_kegg),
                "pert_kegg_count_bin": count_bin(len(pert_kegg)),
                "gene_kegg_count_bin": count_bin(len(gene_kegg)),
                "pert_string_partner_count": len(pert_inter.get("partners") or []),
                "gene_string_partner_count": len(gene_inter.get("partners") or []),
                "pert_string_partner_count_bin": count_bin(len(pert_inter.get("partners") or [])),
                "gene_string_partner_count_bin": count_bin(len(gene_inter.get("partners") or [])),
                "functional_closeness_score": closeness_score,
                "functional_closeness_score_bin": "3+" if closeness_score >= 3 else str(closeness_score),
                "functional_closeness_level": closeness_level(closeness_score),
            }
        )

    print(f"[features] Built feature rows: {len(rows)}")
    return pd.DataFrame(rows)


def summarize_feature(feature_df: pd.DataFrame, feature: str, baseline: pd.Series) -> pd.DataFrame:
    rows = []
    grouped = feature_df.groupby(feature, dropna=False, sort=True)
    for value, group in grouped:
        counts = group["label"].value_counts().reindex(LABELS, fill_value=0)
        total = len(group)
        row = {
            "feature": feature,
            "value": str(value),
            "n": total,
            "coverage_pct": total / len(feature_df) * 100,
        }
        max_abs_lift = 0.0
        directional_lift = 0.0
        for label in LABELS:
            pct = counts[label] / total * 100 if total else 0.0
            lift = pct - baseline[label]
            row[f"{label}_count"] = int(counts[label])
            row[f"{label}_pct"] = pct
            row[f"{label}_lift"] = lift
            max_abs_lift = max(max_abs_lift, abs(lift))
            if label in {"up", "down"}:
                directional_lift += max(0.0, lift)
        row["max_abs_lift"] = max_abs_lift
        row["positive_directional_lift"] = directional_lift
        rows.append(row)
    return pd.DataFrame(rows)


def rank_features(summary_df: pd.DataFrame) -> pd.DataFrame:
    print("[rank] Ranking features by lift and support...")
    eligible = summary_df[summary_df["n"] >= 20].copy()
    ranked = (
        eligible.groupby("feature")
        .agg(
            max_abs_lift=("max_abs_lift", "max"),
            best_directional_lift=("positive_directional_lift", "max"),
            largest_bucket=("n", "max"),
            buckets=("value", "count"),
        )
        .reset_index()
        .sort_values(["max_abs_lift", "best_directional_lift"], ascending=False)
    )
    return ranked


def recommendation_for(feature: str, rows: pd.DataFrame) -> str:
    eligible = rows[rows["n"] >= 20]
    max_lift = float(eligible["max_abs_lift"].max()) if len(eligible) else 0.0
    max_directional = float(eligible["positive_directional_lift"].max()) if len(eligible) else 0.0
    if feature == "target_in_pert_string" and rows["n"].max() < 50:
        return "maybe include: strong biological signal, but low direct-hit count"
    if max_lift >= 12 or max_directional >= 12:
        return "include"
    if max_lift >= 6 or max_directional >= 6:
        return "maybe include"
    return "exclude or use only as support"


def make_markdown_report(
    feature_df: pd.DataFrame,
    summary_df: pd.DataFrame,
    ranked_df: pd.DataFrame,
) -> str:
    baseline_counts = feature_df["label"].value_counts().reindex(LABELS, fill_value=0)
    baseline_pct = baseline_counts / len(feature_df) * 100

    feature_order = [
        "target_in_pert_string",
        "string_score_bin",
        "shared_go",
        "shared_go_count",
        "go_jaccard_bin",
        "shared_kegg",
        "shared_kegg_count",
        "gene_has_summary",
        "gene_has_go",
        "gene_has_kegg",
        "gene_is_uncharacterized",
        "gene_annotation_strength",
        "pert_has_summary",
        "pert_has_go",
        "pert_has_kegg",
        "pert_is_uncharacterized",
        "pert_annotation_strength",
        "pert_go_count_bin",
        "gene_go_count_bin",
        "pert_kegg_count_bin",
        "gene_kegg_count_bin",
        "pert_string_partner_count_bin",
        "gene_string_partner_count_bin",
        "functional_closeness_score_bin",
        "functional_closeness_level",
    ]

    lines = [
        "# Enrichment Feature EDA Report",
        "",
        "## Baseline",
        "",
        f"- Rows: {len(feature_df)}",
        f"- `none`: {baseline_counts['none']} ({baseline_pct['none']:.1f}%)",
        f"- `up`: {baseline_counts['up']} ({baseline_pct['up']:.1f}%)",
        f"- `down`: {baseline_counts['down']} ({baseline_pct['down']:.1f}%)",
        "",
        "## Ranked Features",
        "",
        "| rank | feature | max abs lift | best directional lift | largest bucket | buckets |",
        "|---:|---|---:|---:|---:|---:|",
    ]

    for rank, row in enumerate(ranked_df.head(20).itertuples(index=False), start=1):
        lines.append(
            f"| {rank} | `{row.feature}` | {row.max_abs_lift:.1f} | "
            f"{row.best_directional_lift:.1f} | {int(row.largest_bucket)} | {int(row.buckets)} |"
        )

    lines.extend(["", "## Feature Buckets", ""])
    for feature in feature_order:
        part = summary_df[summary_df["feature"] == feature].copy()
        if part.empty:
            continue
        recommendation = recommendation_for(feature, part)
        lines.extend(
            [
                f"### `{feature}`",
                "",
                f"Recommendation: **{recommendation}**",
                "",
                "| value | n | coverage | none | up | down | max lift |",
                "|---|---:|---:|---:|---:|---:|---:|",
            ]
        )
        part = part.sort_values(["n", "value"], ascending=[False, True])
        for row in part.itertuples(index=False):
            lines.append(
                f"| `{row.value}` | {int(row.n)} | {row.coverage_pct:.1f}% | "
                f"{row.none_pct:.1f}% ({row.none_lift:+.1f}) | "
                f"{row.up_pct:.1f}% ({row.up_lift:+.1f}) | "
                f"{row.down_pct:.1f}% ({row.down_lift:+.1f}) | "
                f"{row.max_abs_lift:.1f} |"
            )
        lines.append("")

    lines.extend(
        [
            "## Final Prompt Recommendation",
            "",
            "Include compact feature-style context only:",
            "",
            "```text",
            "Target annotation coverage: strong/medium/weak/uncharacterized",
            "Shared GO biological processes: yes/no; top shared terms if yes",
            "Shared KEGG pathways: yes/no; pathway names if yes",
            "STRING functional association: yes/no/unknown; score if yes",
            "Pert-target functional closeness: low/medium/high",
            "```",
            "",
            "Avoid raw full GO lists, full KEGG lists, full STRING partner lists, and long summaries.",
            "",
            "Important: `STRING not found` should not be treated as proof of `none`; it only means no direct STRING association was found in this cache.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)

    train_df, context = load_inputs(args.train_csv, args.context_json)
    feature_df = build_feature_rows(train_df, context)

    baseline = (
        feature_df["label"].value_counts(normalize=True).reindex(LABELS, fill_value=0) * 100
    )

    features_to_summarize = [
        "target_in_pert_string",
        "string_score_bin",
        "shared_go",
        "shared_go_count",
        "go_jaccard_bin",
        "shared_kegg",
        "shared_kegg_count",
        "gene_has_summary",
        "gene_has_go",
        "gene_has_kegg",
        "gene_is_uncharacterized",
        "gene_annotation_strength",
        "pert_has_summary",
        "pert_has_go",
        "pert_has_kegg",
        "pert_is_uncharacterized",
        "pert_annotation_strength",
        "pert_go_count_bin",
        "gene_go_count_bin",
        "pert_kegg_count_bin",
        "gene_kegg_count_bin",
        "pert_string_partner_count_bin",
        "gene_string_partner_count_bin",
        "functional_closeness_score_bin",
        "functional_closeness_level",
    ]

    print("[summary] Computing bucket label distributions...")
    summary_df = pd.concat(
        [summarize_feature(feature_df, feature, baseline) for feature in features_to_summarize],
        ignore_index=True,
    )
    ranked_df = rank_features(summary_df)
    report = make_markdown_report(feature_df, summary_df, ranked_df)

    rows_path = args.output_dir / "enrichment_feature_rows.csv"
    buckets_path = args.output_dir / "enrichment_feature_buckets.csv"
    ranked_path = args.output_dir / "enrichment_feature_ranked.csv"
    report_path = args.output_dir / "enrichment_feature_eda_report.md"

    print(f"[write] Saving row features: {rows_path}")
    feature_df.to_csv(rows_path, index=False)
    print(f"[write] Saving bucket summary: {buckets_path}")
    summary_df.to_csv(buckets_path, index=False)
    print(f"[write] Saving ranked features: {ranked_path}")
    ranked_df.to_csv(ranked_path, index=False)
    print(f"[write] Saving markdown report: {report_path}")
    report_path.write_text(report, encoding="utf-8")
    print("[done] EDA complete.")


if __name__ == "__main__":
    main()
