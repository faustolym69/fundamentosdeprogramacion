import random

# ==========================================
# CONFIGURACIÓN Y CONSTANTES DEL JUEGO
# ==========================================
MAX_HEALTH = 100
MAX_DEFENSE = 15   # Se reduce la defensa máxima para que entre más daño
MIN_ATTACK = 25    # Daño mínimo de ataque aumentado para asegurar más impacto
MAX_ATTACK = 55    # Daño máximo de ataque aumentado sustancialmente
MAX_RONDAS = 4  # Límite máximo de tiradas de dados para que no sea muy largo
MAX_HEALS = 2     # Número máximo de curaciones por jugador
HEAL_THRESHOLD = 70 # Se usa automáticamente con 30% o más de daño (70 de vida o menos)

# ==========================================
# FUNCIONES AUXILIARES (HERRAMIENTAS)
# ==========================================

def dice():
  """Simula el lanzamiento de un dado de 6 caras."""
  return random.randint(1, 6)

def calc_damage(attack, defense):
  """Calcula el daño infligido restando la defensa al ataque."""
  if attack > defense:
    return attack - defense
  else:
    return 0

def draw_bar(current, max_value, length=10, symbol="█", empty_symbol="░"):
  """Genera una barra de estado visual."""
  current = max(0, current)
  filled_length = int(round(length * current / max_value))
  bar = symbol * filled_length + empty_symbol * (length - filled_length)
  return f"[{bar}] {current}/{max_value}"

def show_status(name, health, defense):
  """Muestra en pantalla la barra de salud y escudo de un jugador."""
  health_bar = draw_bar(health, MAX_HEALTH, symbol="❤", empty_symbol="░")
  defense_bar = draw_bar(defense, MAX_DEFENSE, symbol="⛨", empty_symbol="░")
  print(f"{name} -> Vida: {health_bar}  |  Defensa: {defense_bar}")

def show_dice_face(dice_number):
  """Muestra de forma gráfica la cara de un dado usando caracteres UTF-8."""
  pos1 = pos2 = pos3 = pos4 = pos5 = pos6 = pos7 = False

  if dice_number == 1:
    pos4 = True
  elif dice_number == 2:
    pos1 = pos7 = True
  elif dice_number == 3:
    pos1 = pos4 = pos7 = True
  elif dice_number == 4:
    pos1 = pos2 = pos6 = pos7 = True
  elif dice_number == 5:
    pos1 = pos2 = pos4 = pos6 = pos7 = True
  elif dice_number == 6:
    pos1 = pos2 = pos3 = pos5 = pos6 = pos7 = True

  print("┌─────────┐")
  # Fila 1
  fila1 = "│ " + ("●   " if pos1 else "    ") + ("● │" if pos2 else "  │")
  print(fila1)
  # Fila 2
  fila2 = "│ " + ("● " if pos3 else "  ") + ("● " if pos4 else "  ") + ("● │" if pos5 else "  │")
  print(fila2)
  # Fila 3
  fila3 = "│ " + ("●   " if pos6 else "    ") + ("● │" if pos7 else "  │")
  print(fila3)
  print("└─────────┘")

def chequear_y_curar(player_name, health, heals_left, ronda_actual, historial_curaciones):
  """Detecta automáticamente si el jugador tiene 70 HP o menos y usa una pócima automáticamente."""
  if health <= HEAL_THRESHOLD and heals_left > 0:
    print(f"\n➕ [AUTOMÁTICO] ¡Atención {player_name}! Tu vida ha bajado a {health} HP (límite de seguridad: {HEAL_THRESHOLD} HP).")
    print(f"✨ Usando automáticamente una pócima de salud. Restableciendo vida a {MAX_HEALTH} HP. (Pócimas restantes: {heals_left - 1})")
    # Registrar momento de uso automático de la pócima
    historial_curaciones.append(f"- {player_name} usó automáticamente una pócima en la Ronda {ronda_actual} cuando tenía {health} HP.")
    return MAX_HEALTH, heals_left - 1
  return health, heals_left

# ==========================================
# CONTROLADOR PRINCIPAL DEL JUEGO
# ==========================================

def jugar_partida():
  """Función principal que controla el flujo de la partida."""
  print("=========================================")
  print("       ¡BIENVENIDOS JUGADORES!           ")
  print("=========================================")

  player1_name = input("Ingrese el nombre del primer jugador: ")
  player2_name = input("Ingrese el nombre del segundo jugador: ")

  # Inicialización de estadísticas para la partida actual
  p1_health = MAX_HEALTH
  p2_health = MAX_HEALTH
  p1_heals = MAX_HEALS
  p2_heals = MAX_HEALS
  ronda_actual = 1

  # Historial para almacenar el momento exacto en que usan las pociones
  historial_curaciones = []

  print(f"\n⚔️  {player1_name} VS {player2_name} ⚔️")
  print("--------------------------------------------------")
  show_status(player1_name, p1_health, MAX_DEFENSE)
  show_status(player2_name, p2_health, MAX_DEFENSE)
  print("--------------------------------------------------")
  print(f"¡Comienza el juego! La partida durará un máximo de {MAX_RONDAS} rondas (tiradas de dados).\n")

  # CICLO DE BATALLA PRINCIPAL
  while ronda_actual <= MAX_RONDAS:
    print(f"\n=== RONDA {ronda_actual} / {MAX_RONDAS} ===")

    # Oportunidad de curación antes de los dados
    p1_health, p1_heals = chequear_y_curar(player1_name, p1_health, p1_heals, ronda_actual, historial_curaciones)
    p2_health, p2_heals = chequear_y_curar(player2_name, p2_health, p2_heals, ronda_actual, historial_curaciones)

    # Regla: Si un jugador ya gastó sus 2 pociones y tiene menos vida que el otro, pierde inmediatamente
    if p1_heals == 0 and p1_health < p2_health:
      print(f"\n❌ {player1_name} ha utilizado sus dos pócimas de salud y tiene menos vida que su rival.")
      print(f"🏆 ¡{player2_name} gana la partida por la regla de desgaste!")
      if historial_curaciones:
        print("\n📜 HISTORIAL DE USO DE PÓCIMAS:")
        for evento in historial_curaciones:
          print(evento)
      return
    if p2_heals == 0 and p2_health < p1_health:
      print(f"\n❌ {player2_name} ha utilizado sus dos pócimas de salud y tiene menos vida que su rival.")
      print(f"🏆 ¡{player1_name} gana la partida por la regla de desgaste!")
      if historial_curaciones:
        print("\n📜 HISTORIAL DE USO DE PÓCIMAS:")
        for evento in historial_curaciones:
          print(evento)
      return

    # Pausa antes de lanzar los dados
    input("👉 Presiona Enter para lanzar los dados...")

    p1_dice = dice()
    p2_dice = dice()

    print(f"\n🎲 {player1_name} tira el dado:")
    show_dice_face(p1_dice)

    print(f"🎲 {player2_name} tira el dado:")
    show_dice_face(p2_dice)

    # 1. DEFINICIÓN DE QUIÉN INICIA EL TURNO EN ESTA RONDA
    if p1_dice > p2_dice:
      print(f"💥 ¡Turno de {player1_name}!")
      ataque_aleatorio = random.randint(MIN_ATTACK, MAX_ATTACK)
      damage = calc_damage(ataque_aleatorio, MAX_DEFENSE)
      p2_health -= damage
      print(f"{player1_name} ataca con fuerza {ataque_aleatorio} causando {damage} de daño efectivo (defensa oponente: {MAX_DEFENSE}).")
      show_status(player2_name, p2_health, MAX_DEFENSE)
      print("-" * 30)

      if p2_health <= 0:
        if p2_heals > 0:
          print(f"\n💥 ¡{player2_name} está a punto de caer!")
          p2_health, p2_heals = chequear_y_curar(player2_name, p2_health, p2_heals, ronda_actual, historial_curaciones)

        if p2_health <= 0:
          print(f"\n🏆 ¡{player1_name} gana la partida al derrotar a su oponente!")
          if historial_curaciones:
            print("\n📜 HISTORIAL DE USO DE PÓCIMAS:")
            for evento in historial_curaciones:
              print(evento)
          return

    elif p2_dice > p1_dice:
      print(f"💥 ¡Turno de {player2_name}!")
      ataque_aleatorio = random.randint(MIN_ATTACK, MAX_ATTACK)
      damage = calc_damage(ataque_aleatorio, MAX_DEFENSE)
      p1_health -= damage
      print(f"{player2_name} ataca con fuerza {ataque_aleatorio} causando {damage} de daño efectivo (defensa oponente: {MAX_DEFENSE}).")
      show_status(player1_name, p1_health, MAX_DEFENSE)
      print("-" * 30)

      if p1_health <= 0:
        if p1_heals > 0:
          print(f"\n💥 ¡{player1_name} está a punto de caer!")
          p1_health, p1_heals = chequear_y_curar(player1_name, p1_health, p1_heals, ronda_actual, historial_curaciones)

        if p1_health <= 0:
          print(f"\n🏆 ¡{player2_name} gana la partida al derrotar a su oponente!")
          if historial_curaciones:
            print("\n📜 HISTORIAL DE USO DE PÓCIMAS:")
            for evento in historial_curaciones:
              print(evento)
          return

    else:
      print("⚖️ ¡Empate en los dados! Nadie ataca en esta ronda.\n")

    ronda_actual += 1

  # DETERMINAR GANADOR POR PUNTOS DE VIDA SI SE AGOTAN LAS RONDAS
  print("\n=========================================")
  print("       ¡FIN DE LAS RONDAS!               ")
  print("=========================================")
  print(f"Resultado final:")
  show_status(player1_name, p1_health, MAX_DEFENSE)
  show_status(player2_name, p2_health, MAX_DEFENSE)

  # Comprobaciones finales considerando el uso de pociones
  if p1_heals == 0 and p1_health < p2_health:
    print(f"\n🏆 ¡{player2_name} gana la partida! {player1_name} usó sus dos pócimas y tiene menos vida.")
  elif p2_heals == 0 and p2_health < p1_health:
    print(f"\n🏆 ¡{player1_name} gana la partida! {player2_name} usó sus dos pócimas y tiene menos vida.")
  elif p1_health > p2_health:
    print(f"\n🏆 ¡{player1_name} gana por tener más vida restante!")
  elif p2_health > p1_health:
    print(f"\n🏆 ¡{player2_name} gana por tener más vida restante!")
  else:
    print("\n🤝 ¡Es un empate absoluto en vida!")

  # Mostrar historial final de pócimas utilizadas
  if historial_curaciones:
    print("\n📜 HISTORIAL DE USO DE PÓCIMAS:")
    for evento in historial_curaciones:
      print(evento)
  else:
    print("\n📜 Ningún jugador utilizó pócimas de salud durante la partida.")

# Ejecutar la partida
if __name__ == "__main__":
  jugar_partida()