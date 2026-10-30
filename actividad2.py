
TEMP_SOLIDO = 0
TEMP_GAS = 100

temp = 70

print(f"Temperatura evaluada: {temp} °C")
if temp > TEMP_SOLIDO and temp < TEMP_GAS:
  print("El agua está en estado líquido")
else:
  print("El agua no está en estado líquido")