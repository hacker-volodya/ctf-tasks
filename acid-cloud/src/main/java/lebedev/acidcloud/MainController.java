package lebedev.acidcloud;

import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.io.InputStreamReader;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.attribute.FileAttribute;
import java.nio.file.attribute.PosixFilePermission;
import java.nio.file.attribute.PosixFilePermissions;
import java.util.Set;
import java.util.concurrent.TimeUnit;

@Controller
public class MainController {
    @PostMapping("/")
    String run(@RequestParam("file") MultipartFile file, Model model) throws IOException, InterruptedException {
        Set<PosixFilePermission> rx = PosixFilePermissions.fromString("rwxr-xr-x");
        FileAttribute<?> permissions = PosixFilePermissions.asFileAttribute(rx);
        Path tempDirectory = Files.createTempDirectory(null, permissions);
        Path tempFile = tempDirectory.resolve("Main.class");
        file.transferTo(tempFile.toFile());
        Process p = Runtime.getRuntime().exec(new String[]{"/app/executor", tempDirectory.toAbsolutePath().toString()});
        String result = "";
        if (!p.waitFor(5, TimeUnit.SECONDS)) {
            result += "Timeout reached\n\n";
        }
        try {
            Files.delete(tempFile);
            Files.delete(tempDirectory);
        } catch (Exception e) {
            System.err.println(e);
        }
        char[] stdout = new char[4096];
        int stdoutLen = (new InputStreamReader(p.getInputStream())).read(stdout);
        if (stdoutLen > 0) {
            result += new String(stdout, 0, stdoutLen);
        }
        char[] stderr = new char[4096];
        int stderrLen = (new InputStreamReader(p.getErrorStream())).read(stderr);
        if (stderrLen > 0) {
            result += new String(stderr, 0, stderrLen);
        }
        model.addAttribute("result", result);
        return "index";
    }

    @GetMapping("/")
    String index(Model model) {
        model.addAttribute("result", "");
        return "index";
    }
}
