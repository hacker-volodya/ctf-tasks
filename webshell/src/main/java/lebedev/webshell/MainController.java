package lebedev.webshell;

import org.springframework.expression.Expression;
import org.springframework.expression.ExpressionParser;
import org.springframework.expression.common.TemplateParserContext;
import org.springframework.expression.spel.standard.SpelExpressionParser;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.concurrent.TimeUnit;

@Controller
public class MainController {
    @PostMapping("/")
    String runShell(@RequestParam("command") String command, Model model) throws IOException, InterruptedException {
        Process p = Runtime.getRuntime().exec(new String[]{"/bin/su", "restricted", "-c", command}, new String[0], new File("/"));
        String result = "";
        if (!p.waitFor(5, TimeUnit.SECONDS)) {
            result += "Timeout reached\n\n";
        }
        char[] stdout = new char[4096];
        int stdoutLen = (new InputStreamReader(p.getInputStream())).read(stdout);
        char[] stderr = new char[4096];
        int stderrLen = (new InputStreamReader(p.getErrorStream())).read(stderr);
        if (stdoutLen > 0) {
            result += "Stdout:\n" + new String(stdout, 0, stdoutLen) + "\n";
        }
        if (stderrLen > 0) {
            result += "Stderr:\n" + new String(stderr, 0, stderrLen) + "\n";
        }
        ExpressionParser parser = new SpelExpressionParser();
        Expression exp = parser.parseExpression(String.format("#{T(java.time.Clock).systemUTC().instant().toString()} %s", command), new TemplateParserContext());
        AuditLog.addEntry(exp);
        model.addAttribute("result", result);
        return "index";
    }

    @GetMapping("/")
    String index(Model model) {
        model.addAttribute("result", "");
        return "index";
    }
}
