# I2P(I) 2025 Final Project: Monster Go

### Final Project for National Tsing Hua University Introduction to Programming (I) 114 Fall

*This Project is inspired by classic pokemon game*

Author: Jay Wang (王宥傑)

## About Creativity

1. Day-Night Cycle and lamps (above ```night_overlay```), similar to Minecraft

    Use ```special_flags=pg.BLEND_MULT``` to draw darkness overlay

```python
l_r, l_g, l_b = 40, 40, 150
h_r, h_g, h_b = 255, 255, 255
cycle_duration = 60 # seconds

r = l_r + (h_r - l_r) * ((math.sin((2*3.1415/cycle_duration)*self.game_time))+1)/2
g = l_g + (h_g - l_g) * ((math.sin((2*3.1415/cycle_duration) * self.game_time))+1)/2
b = l_b + (h_b - l_b) * ((math.sin((2*3.1415/cycle_duration) * self.game_time))+1)/2

r = int(r)
g = int(g)
b = int(b)

darkness = pg.Surface(screen.get_size())
darkness.fill((r, g, b))
screen.blit(darkness, (0, 0), special_flags=pg.BLEND_MULT)
```

## About Checkpoint 3

---

### 1. New map (Done)
A new 15x10 map where player can teleport
### 2. Shop (Done)
Buy and sell surface
### 3. Online interaction (Done except chat overlay)
Send direction in change 
### 4. Advance battle
- heal potion: +50% of hp
- defense potion: -50% of opponent's attack
- strength potion: +50% of damage

```
damage = monster_level * efficiency * 2
```
where efficiency is subject to potions.
### 5. Minimap (Done)
max width of 200 minimap
### 6. Navigation  (Done)
use bfs to search the shortest path