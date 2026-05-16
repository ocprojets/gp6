import matplotlib.pyplot as plt

with open('mic1k.csv') as f:
    values = [int(l.strip()) for l in f if l.strip()]

center = sum(values) // len(values)
ecarts = [abs(v - center) for v in values]
peak = max(ecarts)

print(f"Centre : {center}")
print(f"Pic max (écart) : {peak}")
print(f"Seuil conseillé (70%) : {int(peak * 0.7)}")

plt.figure(figsize=(14, 4))
plt.plot(ecarts, linewidth=0.5)
plt.axhline(int(peak * 0.7), color='red', linestyle='--', label=f'Seuil suggéré ({int(peak*0.7)})')
plt.xlabel('Échantillon (1500/s)')
plt.ylabel('Écart au centre')
plt.title('Amplitude du signal — clap visible?')
plt.legend()
plt.tight_layout()
plt.savefig('mic1k.png')
plt.show()