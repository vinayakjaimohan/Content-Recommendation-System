package com.contentrecomendation.backend.repository;

import com.contentrecomendation.backend.model.Recommendation;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface RecommendationRepository extends JpaRepository<Recommendation, Long> {
    List<Recommendation> findByUserId(Long userId);

    List<Recommendation> findByCategoryIn(List<String> interestNames);
    
    List<Recommendation> findByCategory(String category);
    
    List<Recommendation> findByGenre(String genre);
    
    List<Recommendation> findByCategoryAndGenre(String category, String genre);
}
