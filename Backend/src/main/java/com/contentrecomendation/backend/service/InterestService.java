package com.contentrecomendation.backend.service;

import com.contentrecomendation.backend.model.Interest;

import java.util.List;

public interface InterestService {
    Interest addInterest(Long userId, Interest interest);
    List<Interest> getUserInterests(Long userId);

    Interest saveInterest(Interest interest);

    List<Interest> getInterestsByUserId(Long userId);

    void deleteInterest(Long id);
}
