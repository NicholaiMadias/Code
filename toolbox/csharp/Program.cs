var chars = string.Join(" ", args).ToCharArray();
Array.Reverse(chars);
Console.WriteLine(new string(chars));
