const roll = (): number => Math.floor(Math.random() * 6) + 1;
const a = roll();
const b = roll();
console.log(`Rolled ${a} + ${b} = ${a + b}${a === b ? " - Doubles! You win!" : ""}`);
