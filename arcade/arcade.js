#!/usr/bin/env node
"use strict";

/** Roll two six-sided dice; doubles are a win. */
const roll = () => Math.floor(Math.random() * 6) + 1;
const first = roll();
const second = roll();
const result = `Rolled ${first} + ${second} = ${first + second}${first === second ? " - Doubles! You win!" : ""}`;
console.log(result);
