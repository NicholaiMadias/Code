# Nexus Toolbox and Arcade

Five small reference implementations share the same behavior across Python, JavaScript, PowerShell, Ruby, and Go. The Toolbox reverses the combined input text; the Arcade rolls two dice and reports doubles as a win. Java, C#, and TypeScript ports remain available for comparison.

| Language | Toolbox | Arcade |
| --- | --- | --- |
| Python | `python toolbox/toolbox.py hello world` | `python arcade/arcade.py` |
| JavaScript | `node toolbox/toolbox.js hello world` | `node arcade/arcade.js` |
| PowerShell | `pwsh toolbox/toolbox.ps1 hello world` | `pwsh arcade/arcade.ps1` |
| Ruby | `ruby toolbox/toolbox.rb hello world` | `ruby arcade/arcade.rb` |
| Go | `go run toolbox/toolbox.go hello world` | `go run arcade/arcade.go` |
| Java | `java toolbox/Toolbox.java hello` | `java arcade/Arcade.java` |
| C# | `dotnet run --project toolbox/csharp -- hello` | `dotnet run --project arcade/csharp` |
| TypeScript | `npx tsx toolbox/toolbox.ts hello` | `npx tsx arcade/arcade.ts` |

The five primary ports keep the same command-line contract so they can be used as small learning exercises in the Nexus LMS and Toolbox. They do not need API keys, hosted services, or network access.
