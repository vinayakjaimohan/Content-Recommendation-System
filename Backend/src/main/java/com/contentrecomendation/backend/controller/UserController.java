package com.contentrecomendation.backend.controller;

import com.contentrecomendation.backend.model.User;
import com.contentrecomendation.backend.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;
import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api")
public class UserController {

    @Autowired
    private UserService userService;

    @PostMapping("/auth/register")
    public ResponseEntity<?> register(@Valid @RequestBody User user) {
        try {
            User newUser = userService.registerUser(user);
            return ResponseEntity.ok(newUser);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(Map.of("message", e.getMessage()));
        } catch (Exception e) {
            return ResponseEntity.status(500).body(Map.of("message", "Registration failed due to server error: " + e.getMessage()));
        }
    }

    @PostMapping("/auth/login")
    public ResponseEntity<?> login(@RequestBody User user) {
        try {
            Map<String, Object> loginResponse = userService.loginUser(user.getEmail(), user.getPassword());
            return ResponseEntity.ok(loginResponse);
        } catch (IllegalArgumentException e) {
            return ResponseEntity.badRequest().body(e.getMessage());
        } catch (Exception e) {
            return ResponseEntity.status(500).body("Login failed due to server error.");
        }
    }

    @GetMapping("/users")
    public ResponseEntity<List<User>> getAllUsers() {
        return ResponseEntity.ok(userService.getAllUsers());
    }

    @GetMapping("/user/profile")
    public ResponseEntity<?> getUserProfile(@RequestHeader("Authorization") String token) {
        try {
            String jwtToken = token.replace("Bearer ", "");
            User user = userService.getUserFromToken(jwtToken);
            return ResponseEntity.ok(Map.of(
                "name", user.getUsername(),
                "email", user.getEmail()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(401).body("Invalid token");
        }
    }

    @PutMapping("/user/profile")
    public ResponseEntity<?> updateUserProfile(@RequestHeader("Authorization") String token, 
                                            @RequestBody Map<String, String> profileData) {
        try {
            String jwtToken = token.replace("Bearer ", "");
            User user = userService.getUserFromToken(jwtToken);
            
            String name = profileData.get("name");
            String email = profileData.get("email");
            String password = profileData.get("password");
            
            User updatedUser = userService.updateUserProfile(user.getId(), name, email, password);
            return ResponseEntity.ok(Map.of(
                "name", updatedUser.getUsername(),
                "email", updatedUser.getEmail()
            ));
        } catch (Exception e) {
            return ResponseEntity.status(400).body("Failed to update profile: " + e.getMessage());
        }
    }

    @DeleteMapping("/user/profile")
    public ResponseEntity<?> deleteUserProfile(@RequestHeader("Authorization") String token) {
        try {
            String jwtToken = token.replace("Bearer ", "");
            User user = userService.getUserFromToken(jwtToken);
            userService.deleteUser(user.getId());
            return ResponseEntity.ok("Profile deleted successfully");
        } catch (Exception e) {
            return ResponseEntity.status(400).body("Failed to delete profile: " + e.getMessage());
        }
    }
}
