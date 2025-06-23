from transformers import GPT2LMHeadModel, GPT2Tokenizer
import torch

# Load pre-trained GPT2 tokenizer and model
model_name = 'gpt2'  # You can use 'gpt2-medium', 'gpt2-large', or 'gpt2-xl' as well
tokenizer = GPT2Tokenizer.from_pretrained(model_name)
model = GPT2LMHeadModel.from_pretrained(model_name)
# Move model to GPU if available
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

# Input prompt
prompt = "in a world of fairies"
input_ids = tokenizer.encode(prompt, return_tensors='pt').to(device)

# Generate output
output = model.generate(
    input_ids,
    max_length=100,
    num_return_sequences=1,
    no_repeat_ngram_size=2,
    do_sample=True,
    top_k=50,
    top_p=0.95,
    temperature=0.9
)

# Decode and print result
generated_text = tokenizer.decode(output[0])
print(generated_text)