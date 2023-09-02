# JADO

A recursive data object that can store arbitrary data.

```py
import jado

j = jado.JADO()
j.name = "John"
j.details = {"hobbies": ["reading", "jogging"]}

print(j.name)
print(j.details.hobbies)
```
