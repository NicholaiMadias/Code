import java.util.Random;

public class Arcade {
    public static void main(String[] args) {
        Random r = new Random();
        int a = r.nextInt(6) + 1, b = r.nextInt(6) + 1;
        System.out.println("Rolled " + a + " + " + b + " = " + (a + b) + (a == b ? " - Doubles! You win!" : ""));
    }
}
