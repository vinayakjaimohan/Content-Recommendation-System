package com.contentrecomendation.backend.repository;

import com.contentrecomendation.backend.model.Interest;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface InterestRepository extends JpaRepository<Interest, Long> {
    List<Interest> findByUserId(Long userId);
}
