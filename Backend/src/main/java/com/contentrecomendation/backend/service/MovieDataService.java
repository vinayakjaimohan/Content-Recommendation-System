package com.contentrecomendation.backend.service;

import com.contentrecomendation.backend.model.Recommendation;
import com.contentrecomendation.backend.repository.RecommendationRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;
import java.util.Random;

@Service
public class MovieDataService {

    @Autowired
    private RecommendationRepository recommendationRepository;

    private final List<Recommendation> movieRecommendations = new ArrayList<>();
    private boolean isLoaded = false;

    public void loadMovieData() {
        if (isLoaded) return;

        try {
            // Create sample movie data since we can't read the large CSV file
            createSampleMovieData();
            isLoaded = true;
        } catch (Exception e) {
            System.err.println("Error loading movie data: " + e.getMessage());
        }
    }

    private void createSampleMovieData() {
        String[] genres = {"Action", "Comedy", "Drama", "Horror", "Romance", "Sci-Fi", "Thriller", "Adventure", "Animation", "Documentary"};
        
        String[] actionMovies = {
            "The Dark Knight", "Mad Max: Fury Road", "John Wick", "Mission: Impossible", "Die Hard",
            "The Matrix", "Gladiator", "Raiders of the Lost Ark", "Terminator 2", "Top Gun"
        };

        String[] comedyMovies = {
            "The Grand Budapest Hotel", "Superbad", "Bridesmaids", "The Hangover", "Shaun of the Dead",
            "Napoleon Dynamite", "Zoolander", "Anchorman", "The 40-Year-Old Virgin", "Groundhog Day"
        };

        String[] dramaMovies = {
            "The Shawshank Redemption", "Forrest Gump", "The Godfather", "Schindler's List", "Pulp Fiction",
            "Fight Club", "Goodfellas", "The Silence of the Lambs", "The Green Mile", "American Beauty"
        };

        String[] horrorMovies = {
            "The Shining", "Halloween", "A Nightmare on Elm Street", "The Exorcist", "Psycho",
            "Alien", "The Thing", "Get Out", "Hereditary", "The Conjuring"
        };

        String[] romanceMovies = {
            "Titanic", "The Notebook", "La La Land", "Eternal Sunshine of the Spotless Mind", "Before Sunrise",
            "500 Days of Summer", "The Princess Bride", "Casablanca", "Gone with the Wind", "When Harry Met Sally"
        };

        String[] scifiMovies = {
            "Blade Runner", "2001: A Space Odyssey", "Star Wars", "Interstellar", "The Martian",
            "Arrival", "Ex Machina", "Her", "District 9", "Children of Men"
        };

        addMoviesToRecommendations(actionMovies, "Action");
        addMoviesToRecommendations(comedyMovies, "Comedy");
        addMoviesToRecommendations(dramaMovies, "Drama");
        addMoviesToRecommendations(horrorMovies, "Horror");
        addMoviesToRecommendations(romanceMovies, "Romance");
        addMoviesToRecommendations(scifiMovies, "Sci-Fi");

        // Save to database
        recommendationRepository.saveAll(movieRecommendations);
    }

    private void addMoviesToRecommendations(String[] movies, String genre) {
        Random random = new Random();
        for (String movie : movies) {
            Recommendation recommendation = new Recommendation();
            recommendation.setTitle(movie);
            recommendation.setCategory(genre);
            recommendation.setDescription("A great " + genre.toLowerCase() + " movie that you'll love!");
            recommendation.setRating(Math.round((3.5 + random.nextDouble() * 1.5) * 10.0) / 10.0);
            recommendation.setImageUrl("https://via.placeholder.com/300x450/cccccc/666666?text=" + movie.replace(" ", "+"));
            movieRecommendations.add(recommendation);
        }
    }

    public List<Recommendation> getMoviesByGenre(String genre) {
        loadMovieData();
        return recommendationRepository.findByCategory(genre);
    }

    public List<Recommendation> getRandomMovies(int count) {
        loadMovieData();
        List<Recommendation> allMovies = recommendationRepository.findAll();
        List<Recommendation> randomMovies = new ArrayList<>();
        Random random = new Random();
        
        for (int i = 0; i < count && i < allMovies.size(); i++) {
            randomMovies.add(allMovies.get(random.nextInt(allMovies.size())));
        }
        
        return randomMovies;
    }
} 