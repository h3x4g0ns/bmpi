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

```go
```

```rust
extern crate jado_rs;

use jado_rs::Jado;

fn main() {
    let mut j = Jado::new();
    j.set("name", "John");
    println!("Name: {:?}", j.get("name"));
}
```
