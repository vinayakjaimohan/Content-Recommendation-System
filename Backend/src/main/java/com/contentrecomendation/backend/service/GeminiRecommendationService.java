package com.contentrecomendation.backend.service;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.stereotype.Service;
import org.springframework.web.client.RestTemplate;

import java.util.*;

@Service
public class GeminiRecommendationService {

    private final RestTemplate restTemplate;

    @Value("${gemini.api.key}")
    private String geminiApiKey;

    @Value("${gemini.api.url}")
    private String geminiApiUrl;

    private final ObjectMapper objectMapper;

    public GeminiRecommendationService(RestTemplate restTemplate) {
        this.restTemplate = restTemplate;
        this.objectMapper = new ObjectMapper();
    }

    public List<Map<String, Object>> getGeminiRecommendations(String contentType, String genre, String preferences, List<Map<String, Object>> watchHistory) {
        System.out.println("=== GEMINI SERVICE CALLED ===");
        System.out.println("Content Type: " + contentType);
        System.out.println("Genre: " + genre);
        System.out.println("Preferences: " + preferences);
        System.out.println("Watch History: " + watchHistory);
        
        try {
            // Build the prompt for Gemini
            String prompt = buildRecommendationPrompt(contentType, genre, preferences, watchHistory);
            
            // Prepare the request body for Gemini API
            Map<String, Object> requestBody = new HashMap<>();
            
            Map<String, Object> contents = new HashMap<>();
            List<Map<String, Object>> parts = new ArrayList<>();
            
            Map<String, Object> part = new HashMap<>();
            part.put("text", prompt);
            parts.add(part);
            
            contents.put("parts", parts);
            requestBody.put("contents", List.of(contents));
            
            // Add generation config for better responses
            Map<String, Object> generationConfig = new HashMap<>();
            generationConfig.put("temperature", 0.7);
            generationConfig.put("topK", 40);
            generationConfig.put("topP", 0.95);
            generationConfig.put("maxOutputTokens", 2048);
            requestBody.put("generationConfig", generationConfig);

            // Set up headers
            HttpHeaders headers = new HttpHeaders();
            headers.setContentType(MediaType.APPLICATION_JSON);
            
            HttpEntity<Map<String, Object>> entity = new HttpEntity<>(requestBody, headers);

            // Make the API call
            String fullUrl = geminiApiUrl + "?key=" + geminiApiKey;
            System.out.println("Calling Gemini API at: " + fullUrl);
            System.out.println("Request body: " + requestBody);
            System.out.println("API Key: " + geminiApiKey.substring(0, 10) + "...");
            
            ResponseEntity<Map> response = restTemplate.postForEntity(fullUrl, entity, Map.class);
            System.out.println("Gemini API response status: " + response.getStatusCode());
            System.out.println("Gemini API response body: " + response.getBody());
            
            if (response.getStatusCode() == HttpStatus.OK && response.getBody() != null) {
                return parseGeminiResponse(response.getBody());
            } else if (response.getStatusCode() == HttpStatus.TOO_MANY_REQUESTS) {
                System.err.println("Gemini API quota exceeded. Using fallback recommendations.");
                System.err.println("Response: " + response.getBody());
                return getFallbackRecommendations(contentType, genre);
            } else {
                System.err.println("Gemini API returned error: " + response.getStatusCode());
                System.err.println("Response: " + response.getBody());
                return getFallbackRecommendations(contentType, genre);
            }
            
        } catch (Exception e) {
            System.err.println("Error calling Gemini API: " + e.getMessage());
            System.err.println("Full error details: " + e.toString());
            e.printStackTrace();
            return getFallbackRecommendations(contentType, genre);
        }
    }

    private String buildRecommendationPrompt(String contentType, String genre, String preferences, List<Map<String, Object>> watchHistory) {
        StringBuilder prompt = new StringBuilder();
        
        prompt.append("You are a content recommendation expert. Based on the following information, provide 5 personalized recommendations in JSON format.\n\n");
        
        prompt.append("Content Type: ").append(contentType).append("\n");
        if (genre != null && !genre.isEmpty()) {
            prompt.append("Preferred Genre: ").append(genre).append("\n");
        }
        
        if (preferences != null && !preferences.isEmpty()) {
            prompt.append("User Preferences: ").append(preferences).append("\n");
        }
        
        if (watchHistory != null && !watchHistory.isEmpty()) {
            prompt.append("Watch History:\n");
            for (Map<String, Object> item : watchHistory) {
                prompt.append("- ").append(item.get("title")).append(" (").append(item.get("type")).append(")");
                if (item.get("rating") != null) {
                    prompt.append(" - Rating: ").append(item.get("rating")).append("/5");
                }
                prompt.append("\n");
            }
        }
        
        prompt.append("\nPlease provide recommendations in this exact JSON format:\n");
        prompt.append("[\n");
        prompt.append("  {\n");
        prompt.append("    \"id\": \"unique_id\",\n");
        prompt.append("    \"title\": \"Title of the content\",\n");
        prompt.append("    \"type\": \"Genre\",\n");
        prompt.append("    \"description\": \"Brief description of why this is recommended\",\n");
        prompt.append("    \"year\": \"Year of release (if applicable)\",\n");
        prompt.append("    \"rating\": \"Average rating if known\"\n");
        prompt.append("  }\n");
        prompt.append("]\n\n");
        prompt.append("Make sure the recommendations are diverse, high-quality, and match the user's preferences and history. Only return valid JSON, no additional text.");
        
        return prompt.toString();
    }

    private List<Map<String, Object>> parseGeminiResponse(Map<String, Object> response) {
        try {
            List<Map<String, Object>> recommendations = new ArrayList<>();
            
            if (response.containsKey("candidates")) {
                List<Map<String, Object>> candidates = (List<Map<String, Object>>) response.get("candidates");
                if (!candidates.isEmpty()) {
                    Map<String, Object> candidate = candidates.get(0);
                    if (candidate.containsKey("content")) {
                        Map<String, Object> content = (Map<String, Object>) candidate.get("content");
                        if (content.containsKey("parts")) {
                            List<Map<String, Object>> parts = (List<Map<String, Object>>) content.get("parts");
                            if (!parts.isEmpty()) {
                                Map<String, Object> part = parts.get(0);
                                String text = (String) part.get("text");
                                
                                System.out.println("Gemini response text: " + text);
                                
                                // Try to extract JSON from the response
                                String jsonText = extractJsonFromText(text);
                                if (jsonText != null) {
                                    System.out.println("Extracted JSON: " + jsonText);
                                    // Parse the JSON response
                                    return parseJsonRecommendations(jsonText);
                                } else {
                                    System.out.println("No JSON found in response, using fallback");
                                    // If no JSON found, create recommendations from the text
                                    return createRecommendationsFromText(text);
                                }
                            }
                        }
                    }
                }
            }
            
            System.out.println("No candidates found in response, using fallback");
            return getFallbackRecommendations("general", "mixed");
            
        } catch (Exception e) {
            System.err.println("Error parsing Gemini response: " + e.getMessage());
            e.printStackTrace();
            return getFallbackRecommendations("general", "mixed");
        }
    }

    private String extractJsonFromText(String text) {
        // Handle markdown code blocks first
        if (text.contains("```json")) {
            int start = text.indexOf("```json") + 7;
            int end = text.indexOf("```", start);
            if (end != -1) {
                return text.substring(start, end).trim();
            }
        }
        
        // Handle regular code blocks
        if (text.contains("```")) {
            int start = text.indexOf("```") + 3;
            int end = text.indexOf("```", start);
            if (end != -1) {
                String content = text.substring(start, end).trim();
                // Check if it looks like JSON
                if (content.startsWith("[") || content.startsWith("{")) {
                    return content;
                }
            }
        }
        
        // Simple JSON extraction - look for content between [ and ]
        int start = text.indexOf('[');
        int end = text.lastIndexOf(']');
        
        if (start != -1 && end != -1 && end > start) {
            return text.substring(start, end + 1);
        }
        
        return null;
    }

    private List<Map<String, Object>> parseJsonRecommendations(String jsonText) {
        try {
            // Parse the JSON response using Jackson
            List<Map<String, Object>> recommendations = objectMapper.readValue(
                jsonText, 
                new TypeReference<List<Map<String, Object>>>() {}
            );
            
            // Validate and clean the recommendations
            return recommendations.stream()
                .filter(rec -> rec.containsKey("title") && rec.containsKey("type"))
                .map(rec -> {
                    Map<String, Object> cleanRec = new HashMap<>();
                    cleanRec.put("id", rec.getOrDefault("id", UUID.randomUUID().toString()));
                    cleanRec.put("title", rec.get("title"));
                    cleanRec.put("type", rec.get("type"));
                    cleanRec.put("description", rec.getOrDefault("description", ""));
                    cleanRec.put("year", rec.getOrDefault("year", ""));
                    cleanRec.put("rating", rec.getOrDefault("rating", ""));
                    return cleanRec;
                })
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
                
        } catch (Exception e) {
            System.err.println("Error parsing JSON recommendations: " + e.getMessage());
            return getFallbackRecommendations("general", "mixed");
        }
    }

    private List<Map<String, Object>> getFallbackRecommendations(String contentType, String genre) {
        List<Map<String, Object>> fallback = new ArrayList<>();
        
        Map<String, List<Map<String, Object>>> recommendationsByType = new HashMap<>();
        
        // Books
        recommendationsByType.put("books", Arrays.asList(
            Map.of("id", "1", "title", "Dune", "type", "Sci-Fi", "description", "Epic science fiction novel", "year", "1965", "rating", "4.5"),
            Map.of("id", "2", "title", "The Hobbit", "type", "Fantasy", "description", "Classic fantasy adventure", "year", "1937", "rating", "4.7"),
            Map.of("id", "3", "title", "Gone Girl", "type", "Thriller", "description", "Psychological thriller", "year", "2012", "rating", "4.2"),
            Map.of("id", "4", "title", "The Shining", "type", "Horror", "description", "Masterpiece of horror", "year", "1977", "rating", "4.4"),
            Map.of("id", "5", "title", "1984", "type", "Drama", "description", "Dystopian classic", "year", "1949", "rating", "4.6")
        ));
        
        // Movies
        recommendationsByType.put("movies", Arrays.asList(
            Map.of("id", "6", "title", "Inception", "type", "Sci-Fi", "description", "Mind-bending sci-fi thriller", "year", "2010", "rating", "4.8"),
            Map.of("id", "7", "title", "The Godfather", "type", "Drama", "description", "Classic crime drama", "year", "1972", "rating", "4.9"),
            Map.of("id", "8", "title", "Interstellar", "type", "Sci-Fi", "description", "Space exploration epic", "year", "2014", "rating", "4.7"),
            Map.of("id", "9", "title", "The Conjuring", "type", "Horror", "description", "Supernatural horror", "year", "2013", "rating", "4.3"),
            Map.of("id", "10", "title", "The Dark Knight", "type", "Action", "description", "Superhero masterpiece", "year", "2008", "rating", "4.9")
        ));
        
        // TV Shows
        recommendationsByType.put("tv", Arrays.asList(
            Map.of("id", "11", "title", "Stranger Things", "type", "Fantasy", "description", "Supernatural mystery series", "year", "2016", "rating", "4.6"),
            Map.of("id", "12", "title", "Breaking Bad", "type", "Drama", "description", "Crime drama masterpiece", "year", "2008", "rating", "4.9"),
            Map.of("id", "13", "title", "The Boys", "type", "Action", "description", "Dark superhero series", "year", "2019", "rating", "4.5"),
            Map.of("id", "14", "title", "Black Mirror", "type", "Sci-Fi", "description", "Technology anthology", "year", "2011", "rating", "4.7"),
            Map.of("id", "15", "title", "The Crown", "type", "Drama", "description", "Royal family drama", "year", "2016", "rating", "4.4")
        ));
        
        // Podcasts
        recommendationsByType.put("podcast", Arrays.asList(
            Map.of("id", "16", "title", "Lore", "type", "Horror", "description", "Dark historical tales", "year", "2015", "rating", "4.5"),
            Map.of("id", "17", "title", "Serial", "type", "Thriller", "description", "True crime investigation", "year", "2014", "rating", "4.8"),
            Map.of("id", "18", "title", "Science Vs", "type", "Sci-Fi", "description", "Science fact vs fiction", "year", "2015", "rating", "4.6"),
            Map.of("id", "19", "title", "This American Life", "type", "Drama", "description", "Human interest stories", "year", "1995", "rating", "4.7"),
            Map.of("id", "20", "title", "Radiolab", "type", "Sci-Fi", "description", "Science and philosophy", "year", "2002", "rating", "4.8")
        ));
        
        List<Map<String, Object>> typeRecommendations = recommendationsByType.getOrDefault(contentType, recommendationsByType.get("movies"));
        
        // Filter by genre if specified
        if (genre != null && !genre.isEmpty() && !genre.equals("mixed")) {
            typeRecommendations = typeRecommendations.stream()
                .filter(rec -> rec.get("type").equals(genre))
                .collect(ArrayList::new, ArrayList::add, ArrayList::addAll);
        }
        
        // If no genre-specific recommendations, return all
        if (typeRecommendations.isEmpty()) {
            typeRecommendations = recommendationsByType.getOrDefault(contentType, recommendationsByType.get("movies"));
        }
        
        return typeRecommendations;
    }

    private List<Map<String, Object>> createRecommendationsFromText(String text) {
        // Create recommendations based on the text response
        List<Map<String, Object>> recommendations = new ArrayList<>();
        
        // Extract movie titles from the text (simple pattern matching)
        String[] lines = text.split("\n");
        int id = 1;
        
        for (String line : lines) {
            line = line.trim();
            if (line.contains("**") && line.contains("**")) {
                // Extract title between ** markers
                int start = line.indexOf("**") + 2;
                int end = line.indexOf("**", start);
                if (end > start) {
                    String title = line.substring(start, end).trim();
                    if (!title.isEmpty()) {
                        Map<String, Object> rec = new HashMap<>();
                        rec.put("id", String.valueOf(id++));
                        rec.put("title", title);
                        rec.put("type", "AI Generated");
                        rec.put("description", "Recommended by Gemini AI");
                        rec.put("year", "");
                        rec.put("rating", "");
                        recommendations.add(rec);
                    }
                }
            }
        }
        
        // If no structured recommendations found, create a generic one
        if (recommendations.isEmpty()) {
            Map<String, Object> rec = new HashMap<>();
            rec.put("id", "1");
            rec.put("title", "AI Recommendation");
            rec.put("type", "AI Generated");
            rec.put("description", text.substring(0, Math.min(text.length(), 100)) + "...");
            rec.put("year", "");
            rec.put("rating", "");
            recommendations.add(rec);
        }
        
        return recommendations;
    }
} 