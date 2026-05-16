package com.contentrecomendation.backend.service;

import com.contentrecomendation.backend.model.Interest;
import com.contentrecomendation.backend.model.User;
import com.contentrecomendation.backend.repository.InterestRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class InterestServiceImpl implements InterestService {

    @Autowired
    private InterestRepository interestRepo;

    @Override
    public Interest addInterest(Long userId, Interest interest) {
        interest.setUser(new User(userId));
        return interestRepo.save(interest);
    }

    @Override
    public List<Interest> getUserInterests(Long userId) {
        return interestRepo.findByUserId(userId);
    }

    @Override
    public Interest saveInterest(Interest interest) {
        return interestRepo.save(interest);
    }

    @Override
    public List<Interest> getInterestsByUserId(Long userId) {
        return interestRepo.findByUserId(userId);
    }

    @Override
    public void deleteInterest(Long id) {
        interestRepo.deleteById(id);
    }


}
