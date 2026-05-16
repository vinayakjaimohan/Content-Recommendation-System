package com.contentrecomendation.backend.controller;

import com.contentrecomendation.backend.model.Interest;
import com.contentrecomendation.backend.service.InterestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/interests")
public class InterestController {

    @Autowired
    private InterestService interestService;

    @PostMapping("/add")
    public ResponseEntity<Interest> addInterest(@RequestBody Interest interest) {
        Interest savedInterest = interestService.saveInterest(interest);
        return ResponseEntity.ok(savedInterest);
    }

    @GetMapping("/user/{userId}")
    public ResponseEntity<List<Interest>> getInterestsByUser(@PathVariable Long userId) {
        List<Interest> interests = interestService.getInterestsByUserId(userId);
        return ResponseEntity.ok(interests);
    }

    @DeleteMapping("/{id}")
    public ResponseEntity<Void> deleteInterest(@PathVariable Long id) {
        interestService.deleteInterest(id);
        return ResponseEntity.noContent().build();
    }
}
