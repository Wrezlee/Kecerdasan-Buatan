import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

nama_model = "taufiqdp/indonesian-sentiment"
tokenizer = AutoTokenizer.from_pretrained(nama_model)
model = AutoModelForSequenceClassification.from_pretrained(nama_model)

kelas = ['negatif', 'netral', 'positif']

kalimat = input("Masukkan kalimat : ")

inputs = tokenizer(kalimat, return_tensors="pt", truncation=True)
with torch.no_grad():
    logits = model(**inputs).logits

prob = torch.softmax(logits, dim=-1)[0]
idx = int(prob.argmax())

print("\nHASIL PREDIKSI")
print("Kalimat  :", kalimat)
print("Sentimen :", kelas[idx])
print("Keyakinan: {:.2%}".format(prob[idx].item()))