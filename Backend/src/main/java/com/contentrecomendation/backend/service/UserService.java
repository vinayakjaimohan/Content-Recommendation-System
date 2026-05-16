package com.contentrecomendation.backend.service;

import com.contentrecomendation.backend.model.User;

import java.util.List;
import java.util.Map;
import java.util.Optional;

public interface UserService {
    User registerUser(User user);
    Optional<User> getUserByEmail(String email);
    Map<String, Object> loginUser(String email, String password);
    List<User> getAllUsers();
    User getUserFromToken(String token);
    User updateUserProfile(Long userId, String name, String email, String password);
    void deleteUser(Long userId);
}
