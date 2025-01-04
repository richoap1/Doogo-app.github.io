<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Profile</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='public/css/styles.css') }}">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head>
<body>

<header class="bg-custom text-white">
        <div class="container d-flex align-items-center justify-content-between py-2">
            <!-- Logo on the left -->
            <a href="/" class="logo-link">
                <img class="logo" src="{{ url_for('static', filename='public/images/logo.png') }}" alt="Logo" />
            </a>
    
            <!-- Search Bar -->
            <div class="search-bar mx-auto">
                <input type="text" class="form-control" placeholder="Cari Di Doogo" aria-label="Search">
                <button class="btn btn-primary" type="button">Search</button>
            </div>
    
            <!-- User Account Options -->
            <div class="ml-3 d-flex align-items-center">
                {% if session.get('user_id') %}
                <div class="nav-item dropdown">
                    <a class="nav-link dropdown-toggle text-white" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                        {{ session.get('name') }}
                    </a>
                    <div class="dropdown-menu" aria-labelledby="navbarDropdown">
                        <a class="dropdown-item" href="/profile">Profile</a>
                        <div class="dropdown-divider"></div>
                        <a class="dropdown-item" href="/logout">Logout</a>
                    </div>
                </div>
                {% else %}
                <div class="nav-item">
                    <a class="btn btn-dark" href="/register">Sign up</a>
                </div>
                <div class="nav-item">
                    <a class="btn btn-dark" href="/login">Sign In</a>
                </div>
                {% endif %}
            </div>
        </div>
    </header>
    
    <!-- Navigation Links -->
    <nav class="navbar navbar-expand-lg navbar-light bg-light mt-3">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link text-dark" href="/layanan">Layanan Kami</a></li>
                <li class="nav-item"><a class="nav-link text-dark" href="/about">Tentang Kami</a></li>
                <li class="nav-item"><a class="nav-link text-dark" href="/products">Shopping</a></li>
                <li class="nav-item"><a class="nav-link text-dark" href="/bantuan">Bantuan</a></li>
                <li class="nav-item"><a class="nav-link text-dark" href="#">Blog</a></li>
            </ul>
        </div>
    </nav>

<div class="container mt-5">
    <h2 class="text-center">User Profile</h2>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">Email: {{ user.email }}</h5>
            <p class="card-text"><strong>Name:</strong> {{ user.name }}</p>
            <p class="card-text"><strong>Address:</strong> {{ user.address }}</p>
            <p class="card-text"><strong>Gender:</strong> {{ user.gender }}</p>
            <p class="card-text"><strong>Role:</strong> {{ user.role }}</p>
        </div>
    </div>
</div>

<script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
