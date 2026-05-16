package com.contentrecomendation.backend.service;

import com.contentrecomendation.backend.model.User;
import com.contentrecomendation.backend.repository.UserRepository;
import com.contentrecomendation.backend.security.JwtUtil;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;

@Service
public class UserServiceImpl implements UserService {
    @Autowired
    private UserRepository userRepo;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private JwtUtil jwtUtil;

    @Override
    public User registerUser(User user) {
        // Check if user already exists
        if (userRepo.findByUsername(user.getUsername()).isPresent()) {
            throw new IllegalArgumentException("Username already exists");
        }
        if (userRepo.findByEmail(user.getEmail()).isPresent()) {
            throw new IllegalArgumentException("Email already exists");
        }

        // Encode password before saving
        user.setPassword(passwordEncoder.encode(user.getPassword()));
        return userRepo.save(user);
    }

    @Override
    public Optional<User> getUserByEmail(String email) {
        return userRepo.findByEmail(email);
    }

    @Override
    public Map<String, Object> loginUser(String email, String password) {
        Optional<User> userOpt = userRepo.findByEmail(email);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            if (passwordEncoder.matches(password, user.getPassword())) {
                String token = jwtUtil.generateToken(user.getUsername());
                Map<String, Object> response = new HashMap<>();
                response.put("token", token);
                response.put("user", user);
                return response;
            }
        }
        throw new IllegalArgumentException("Invalid email or password");
    }

    @Override
    public List<User> getAllUsers() {
        return userRepo.findAll();
    }

    @Override
    public User getUserFromToken(String token) {
        String username = jwtUtil.extractUsername(token);
        Optional<User> userOpt = userRepo.findByUsername(username);
        if (userOpt.isPresent()) {
            return userOpt.get();
        }
        throw new IllegalArgumentException("Invalid token");
    }

    @Override
    public User updateUserProfile(Long userId, String name, String email, String password) {
        Optional<User> userOpt = userRepo.findById(userId);
        if (userOpt.isPresent()) {
            User user = userOpt.get();
            
            if (name != null && !name.trim().isEmpty()) {
                user.setUsername(name);
            }
            if (email != null && !email.trim().isEmpty()) {
                user.setEmail(email);
            }
            if (password != null && !password.trim().isEmpty()) {
                user.setPassword(passwordEncoder.encode(password));
            }
            
            return userRepo.save(user);
        }
        throw new IllegalArgumentException("User not found");
    }

    @Override
    public void deleteUser(Long userId) {
        if (userRepo.existsById(userId)) {
            userRepo.deleteById(userId);
        } else {
            throw new IllegalArgumentException("User not found");
        }
    }
}
