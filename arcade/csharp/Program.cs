var rng = new Random();
int a = rng.Next(1, 7), b = rng.Next(1, 7);
Console.WriteLine($"Rolled {a} + {b} = {a + b}{(a == b ? " - Doubles! You win!" : "")}");
