package com.liveprism.liveprism_gui.Service;

import org.springframework.core.ParameterizedTypeReference;
import org.springframework.core.io.FileSystemResource;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.util.*;
import org.springframework.web.client.RestTemplate;

import java.io.File;
import java.io.IOException;
import java.io.UncheckedIOException;
import java.nio.file.Files;
import java.util.Base64;
import java.util.Map;

@Service
public class ImageService {
    private final RestTemplate restTemplate = new RestTemplate();

    public File sendImageToPython(String imagePath) {
        File file = new File(imagePath);

        // Prepare multipart request
        MultiValueMap<String, Object> body = new LinkedMultiValueMap<>();
        body.add("file", new FileSystemResource(file));

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.MULTIPART_FORM_DATA);

        HttpEntity<MultiValueMap<String, Object>> requestEntity = new HttpEntity<>(body, headers);

        // Call Python API
        ResponseEntity<Map<String, String>> response = restTemplate.exchange(
                "http://127.0.0.1:8000/segment",
                HttpMethod.POST,
                requestEntity,
                new ParameterizedTypeReference<Map<String, String>>() {
                }
        );

        // Decode mask from response
        String maskBase64 = response.getBody().get("mask");
        byte[] maskBytes = Base64.getDecoder().decode(maskBase64);

        try {
            File out = new File("mask.png");
            Files.write(out.toPath(), maskBytes);
            return out;
        } catch (IOException e) {
            throw new UncheckedIOException(e);
        }
    }
}
