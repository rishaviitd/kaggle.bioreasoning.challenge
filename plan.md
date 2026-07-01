1. task-one -> nvidia api that is unlimited acess to the oss 120b model, we will first need to split the train into (gepa, train, dev, test)
2. the solution of the train data is important it has to be written beforehand so that the prompt optimization can find the correct prompts
3. first thing is benchmarking which model is actaully better for writing this solution are there other models -> paid frontier models -> claude, openai, grok -> on 100 questions to see which one is better -> this can even tell us which can be our refiner model
4. my plan here to build an agent that keep improving the prompt att by itself here the student llm will be the same as the refiner LLM

so for task one two core tasks is for selecting the teacher model for

1. refinement of the prompt
2. writing of the solutions

so we will see here what is the qwality of these candidate renfinement models on 100 stratified questions set we will have to use open router for this though

solution generation will be important because we will need those for the
