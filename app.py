from flask import Flask, request, jsonify
import tiktoken
import time
from typing import List, Tuple

app = Flask(__name__)

class TikTokenizer:
    def __init__(self, model: str = "gpt-3.5-turbo"):
        self.encoding = tiktoken.encoding_for_model(model)

    def tokenize(self, text: str) -> List[int]:
        return self.encoding.encode(text)

    def detokenize(self, tokens: List[int]) -> str:
        return self.encoding.decode(tokens)

    def count_tokens(self, text: str) -> int:
        return len(self.tokenize(text))

    def word_count(self, text: str) -> int:
        return len(text.split())

    def token_details(self, text: str) -> List[Tuple[int, str, int]]:
        tokens = self.tokenize(text)
        decoded_tokens = [self.encoding.decode([token]) for token in tokens]
        token_lengths = [len(decoded_token) for decoded_token in decoded_tokens]
        return list(zip(tokens, decoded_tokens, token_lengths))

    def tokenize_with_time(self, text: str) -> Tuple[List[int], float]:
        start_time = time.time()
        tokens = self.tokenize(text)
        elapsed_time = time.time() - start_time
        return tokens, elapsed_time

@app.route('/tokenize', methods=['POST'])
def tokenize_text():
    data = request.get_json()
    text = data.get('text', '')

    if not text:
        return jsonify({"error": "No text provided"}), 400

    tokenizer = TikTokenizer(model="gpt-3.5-turbo")
    tokens, time_taken = tokenizer.tokenize_with_time(text)

    response = {
        "input_text": text,
        "word_count": tokenizer.word_count(text),
        "token_count": tokenizer.count_tokens(text),
        "time_taken": f"{time_taken:.6f} seconds",
        "tokens": tokens,
        "token_details": [
            {"token_id": token_id, "character": char, "length": length}
            for token_id, char, length in tokenizer.token_details(text)
        ],
        "detokenized_text": tokenizer.detokenize(tokens)
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
