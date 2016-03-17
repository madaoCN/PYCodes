<html>
    <head>
        <title>Burt's Books – Book Detail</title>
        <script src="//ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js"
            type="text/javascript"></script>
        <script src="{{ static_url('scripts/inventory.js') }}"
            type="application/javascript"></script>
    </head>

    <body>
        <div>
            <h1>Burt's Books</h1>

            <hr/>
            <p><h2>The Definitive Guide to the Internet</h2>
            <em>Anonymous</em></p>
        </div>

        <img src="static/images/internet.jpg" alt="The Definitive Guide to the Internet" />

        <hr />

        <input type="hidden" id="session" value="{{ session }}" />
        <div id="add-to-cart">
            <p><span style="color: red;">Only <span id="count">{{ count }}</span>
                left in stock! Order now!</span></p>
            <p>$20.00 <input type="submit" value="Add to Cart" id="add-button" /></p>
        </div>
        <div id="remove-from-cart" style="display: none;">
            <p><span style="color: green;">One copy is in your cart.</span></p>
            <p><input type="submit" value="Remove from Cart" id="remove-button" /></p>
        </div>
    </body>
</html>