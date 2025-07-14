import os

input_file = "knowledge_base/instructions.txt"
output_file = "knowledge_base/qa_context.txt"

# Simple rule-based example: Convert each sentence to a Q&A
def generate_qa(sentence):
    question = f"What should I do in this step: '{sentence[:30]}...'"
    answer = sentence
    return question, answer

with open(input_file, "r", encoding="utf-8") as f:
    lines = f.readlines()

qa_pairs = []

for line in lines:
    line = line.strip()
    if not line:
        continue
    question, answer = generate_qa(line)
    qa_pairs.append(f"Q: {question}\nA: {answer}\n")

with open(output_file, "w", encoding="utf-8") as f:
    f.writelines(qa_pairs)

print("✅ Q&A context saved to qa_context.txt")
