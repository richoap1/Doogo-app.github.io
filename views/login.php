<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" href="{{ url_for('static', filename='public/css/styles.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='public/css/chat.css') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='public/css/form.css') }}">
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.1/aos.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
</head>
<body>

<!-- Header -->
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
    

    <nav class="navbar navbar-expand-lg navbar-light mt-3">
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item"><a class="nav-link text-white" href="/layanan">Layanan Kami</a></li>
                <li class="nav-item"><a class="nav-link text-white" href="/about">Tentang Kami</a></li>
                <li class="nav-item"><a class="nav-link text-white" href="/products">Shopping</a></li>
                <li class="nav-item"><a class="nav-link text-white" href="/bantuan">Bantuan</a></li>
                <li class="nav-item"><a class="nav-link text-white" href="#">Blog</a></li>
            </ul>
        </div>
    </nav>

    <div class="container mt-5" data-aos="fade-up">
    <h2 class="text-center">Login to your account</h2>
    
    <a href="{{ url_for('google.login') }}" class="btn btn-light social-btn">
        <span class="iconify" data-icon="akar-icons:google-fill" style="width: 16px; height: 16px;"></span> Google
    </a>
    <a href="{{ url_for('facebook.login') }}" class="btn btn-light social-btn">
        <span class="iconify" data-icon="akar-icons:facebook-fill" style="width: 16px; height: 16px;"></span> Facebook
    </a>
    <p class="text-center">Or</p>
    
    
    <!-- Display error message if it exists -->
    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}

    <form action="{{ url_for('login') }}" method="post">
        <input type="email" class="form-control" name="username" placeholder="Email" required>
        <input type="password" class="form-control" name="password" placeholder="Password" required>
        <button type="submit" class="btn btn-primary">Login</button>
    </form>
    
    <div class="footer-text">
        <p>Belum mempunyai akun? <a href="{{ url_for('register') }}">Daftar</a></p>
    </div>
</div>
</div>

<!-- Footer -->
<footer class="bg-custom text-white">
        <div class="container">
            <div class="row">
                <div class="col-lg-3 col-md-6 col-sm-6">
                    <div class="footer-menu">
                        <img src="{{ url_for('static', filename='public/images/logo.png') }}" width="200" height="200" alt="logo">
                        <div class="social-links mt-3">
                            <ul class="d-flex list-unstyled gap-2">
                                <li>
                                    <a href="#" class="btn btn-outline-light">
                                        <span class="iconify" data-icon="akar-icons:facebook-fill" style="width: 16px; height: 16px;"></span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="btn btn-outline-light">
                                        <span class="iconify" data-icon="akar-icons:twitter-fill" style="width: 16px; height: 16px;"></span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="btn btn-outline-light">
                                        <span class="iconify" data-icon="akar-icons:youtube-fill" style="width: 16px; height: 16px;"></span>
                                    </a>
                                </li>
                                <li>
                                    <a href="#" class="btn btn-outline-light">
                                        <span class="iconify" data-icon="akar-icons:instagram-fill" style="width: 16px; height: 16px;"></span>
                                    </a>
                                </li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-md-2 col-sm-6">
                    <div class="footer-menu">
                        <h5 class="widget-title">Organic</h5>
                        <ul class="menu-list list-unstyled">
                            <li class="menu-item"><a href="/about" class="nav-link">About us</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Conditions</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Our Journals</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Careers</a></li>
                            <li class="menu-item"><a href="/seller" class="nav-link">Login Seller</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Ultras Press</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-2 col-sm-6">
                    <div class="footer-menu">
                        <h5 class="widget-title">Quick Links</h5>
                        <ul class="menu-list list-unstyled">
                            <li class="menu-item"><a href="#" class="nav-link">Offers</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Discount Coupons</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Stores</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Track Order</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Shop</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Info</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-md-2 col-sm-6">
                    <div class="footer-menu">
                        <h5 class="widget-title">Customer Service</h5>
                        <ul class="menu-list list-unstyled">
                            <li class="menu-item"><a href="#" class="nav-link">FAQ</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Contact</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Privacy Policy</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Returns &amp; Refunds</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Cookie Guidelines</a></li>
                            <li class="menu-item"><a href="#" class="nav-link">Delivery Information</a></li>
                        </ul>
                    </div>
                </div>
                <div class="col-lg-3 col-md-6 col-sm-6">
                    <div class="footer-menu">
                        <h5 class="widget-title">Subscribe Us</h5>
                        <p>Subscribe to our newsletter to get updates about our grand offers.</p>
                        <form class="d-flex mt-3 gap-0" action="/">
                            <input class="form-control rounded-start rounded-0 bg-light" type="email" placeholder="Email Address" aria-label="Email Address">
                            <button class="btn btn-dark rounded-end rounded-0" type="submit">Subscribe</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="text-center py-3">
            <p class="Copyright2023PtDoogoIndonesiaAllRightsReserved">Copyright @ 2023 PT. DOOGO INDONESIA. All Rights Reserved</p>
        </div>
    </footer>

<script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
<script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.1/aos.js"></script>
<script src="https://code.iconify.design/1/1.0.0/iconify.min.js"></script>
<script>
    AOS.init();
</script>
<script src="{{ url_for('static', filename='js/chat.js') }}"></script>

</body>
</html>
