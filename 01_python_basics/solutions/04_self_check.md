# Self-check answers

1. **8 times**: 90, 80, 70, 60, 50, 40, 30, 20. The ninth and tenth calls
   find `battery <= 20` and return early.
2. The last two lines are `battery low`, printed by calls 9 and 10.
3. Change `20` to `30` in `if self.battery <= 20:`. The robot then prints
   battery 90% down to 30%, and `battery low` three times.
