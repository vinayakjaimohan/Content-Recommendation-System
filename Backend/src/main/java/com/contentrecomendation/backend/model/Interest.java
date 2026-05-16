package com.contentrecomendation.backend.model;

import jakarta.persistence.*;

@Entity
public class Interest {

        @Id
        @GeneratedValue(strategy = GenerationType.IDENTITY)
        private Long id;

        private String category;
        private String genre;

        @ManyToOne
        @JoinColumn(name = "user_id")
        private User user;

        // Constructors
        public Interest() {}

        public Interest(String category, String genre, User user) {
                this.category = category;
                this.genre = genre;
                this.user = user;
        }

        // Getters and Setters
        public Long getId() {
                return id;
        }

        public String getCategory() {
                return category;
        }

        public void setCategory(String category) {
                this.category = category;
        }

        public String getGenre() {
                return genre;
        }

        public void setGenre(String genre) {
                this.genre = genre;
        }

        public User getUser() {
                return user;
        }

        public void setUser(User user) {
                this.user = user;
        }
}
