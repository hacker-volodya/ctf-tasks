package lebedev.webshell;

import org.springframework.expression.Expression;

public class AuditLog {
    public static void addEntry(Expression expression) {
        System.out.println(expression.getValue(String.class));
    }
}
