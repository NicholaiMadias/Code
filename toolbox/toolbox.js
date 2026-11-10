#!/usr/bin/env node
"use strict";

/** Reverse the combined command-line text, matching the other Nexus Toolbox ports. */
const text = process.argv.slice(2).join(" ");
process.stdout.write(text ? `${Array.from(text).reverse().join("")}\n` : "");
