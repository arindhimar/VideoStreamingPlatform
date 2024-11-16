// Create notification container
const notifications = {
    init() {
        // Create container for notifications
        const container = document.createElement('div');
        container.id = 'notification-container';
        document.body.appendChild(container);

        // Add styles
        const style = document.createElement('style');
        style.textContent = `
            #notification-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                z-index: 9999;
            }

            .notification {
                background-color: #ffffff;
                color: #ffffff;
                padding: 15px 20px;
                margin-bottom: 10px;
                border-radius: 4px;
                box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
                min-width: 300px;
                max-width: 400px;
                animation: slideIn 0.3s ease-out forwards;
                cursor: pointer;
            }

            .notification.success { background-color: #4caf50; }
            .notification.error { background-color: #f44336; }
            .notification.warning { background-color: #ff9800; }
            .notification.info { background-color: #2196f3; }

            .notification .close-btn {
                background: none;
                border: none;
                color: white;
                cursor: pointer;
                padding: 0 5px;
                font-size: 18px;
                margin-left: 10px;
                opacity: 0.8;
                transition: opacity 0.2s;
            }

            .notification .close-btn:hover {
                opacity: 1;
            }

            @keyframes slideIn {
                from {
                    transform: translateX(100%);
                    opacity: 0;
                }
                to {
                    transform: translateX(0);
                    opacity: 1;
                }
            }

            @keyframes slideOut {
                from {
                    transform: translateX(0);
                    opacity: 1;
                }
                to {
                    transform: translateX(100%);
                    opacity: 0;
                }
            }

            .notification.hiding {
                animation: slideOut 0.3s ease-out forwards;
            }
        `;
        document.head.appendChild(style);
    },

    show(message, type = 'success', duration = 3000) {
        const container = document.getElementById('notification-container');

        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;

        // Create message text
        const text = document.createElement('span');
        text.textContent = message;

        // Create close button
        const closeBtn = document.createElement('button');
        closeBtn.className = 'close-btn';
        closeBtn.innerHTML = '×';
        closeBtn.onclick = (e) => {
            e.stopPropagation();
            this.hide(notification);
        };

        // Assemble notification
        notification.appendChild(text);
        notification.appendChild(closeBtn);
        container.appendChild(notification);

        // Set up auto-dismiss
        setTimeout(() => {
            this.hide(notification);
        }, duration);

        // Click anywhere on notification to dismiss
        notification.onclick = () => {
            this.hide(notification);
        };
    },

    hide(notification) {
        notification.classList.add('hiding');
        setTimeout(() => {
            notification.remove();
        }, 300); // Match the slideOut animation duration
    }
};

// Document ready function
$(document).ready(function () {
    notifications.init();
    // Slide sections on nav link click
    $('.nav-link').on('click', function (e) {
        e.preventDefault();
        const section = $(this).data('section'); // Get the section data attribute

        // Slide up the currently visible section
        $('.section:visible').slideUp(300, function () {
            $('#' + section).slideDown(300, function () {
                if (section === 'anime') fetchAnime();
                if (section === 'genres') fetchGenres();
                if (section === 'episodes') fetchAnime();
                // if (section === 'genres') fetchGenres();

            });
        });
    });

    // Anime functions
    function fetchAnime() {
        $.ajax({
            type: "GET",
            url: "/anime", // Adjust URL to your endpoint
            success: function (response) {
                $('#animeTableBody').empty();
                response.forEach(function (anime) {
                    const newRow = `
                        <tr>
                            <td>${anime.anime_id}</td>
                            <td>${anime.title}</td>
                            <td>${anime.status}</td>
                            <td>${anime.release_date}</td>
                            <td><a style="color:white" href="${anime.thumbnail_url}" target="_blank">View</a></td>
                            <td><a style="color:white" href="${anime.banner_url}" target="_blank">View</a></td>
                            <td>
                                <button class="btn btn-warning btn-sm edit-anime" data-id="${anime.anime_id}">Edit</button>
                                <button class="btn btn-danger btn-sm delete-anime" data-id="${anime.anime_id}">Delete</button>
                            </td>
                        </tr>`;
                    $('#animeTableBody').append(newRow);
                });
            },
            error: function (error) {
                console.error('Error fetching anime:', error);
                notifications.show('Failed to fetch anime list.', 'error');
            }
        });
    }

    $(document).on('click', '.edit-anime', function () {
        const animeId = $(this).data('id');

        // Fetch anime details and open edit modal
        $.ajax({
            type: "GET",
            url: `/anime/${animeId}`, // Adjust URL to your endpoint for fetching anime details
            success: function (anime) {
                // Populate the edit modal with the fetched anime details
                $('#editAnimeId').val(anime.anime_id); // Hidden input for anime ID
                $('#editAnimeTitle').val(anime.title);
                $('#editAnimeSynopsis').val(anime.synopsis);

                // Convert release_date to YYYY-MM-DD format
                const releaseDate = new Date(anime.release_date);
                const formattedDate = releaseDate.toISOString().split('T')[0]; // Get YYYY-MM-DD part
                $('#editAnimeReleaseDate').val(formattedDate);

                $('#editAnimeStatus').val(anime.status);

                // Show the edit modal
                $('#editAnimeModal').modal('show');
            },
            error: function (error) {
                console.error('Error fetching anime details:', error);
                notifications.show('Failed to fetch anime details.', 'error');
            }
        });
    });

    // Handle saving changes in the edit modal
    $('#saveEditAnimeButton').on('click', function () {
        const animeId = $('#editAnimeId').val(); // Get anime ID from hidden input
        const updatedAnimeData = {
            title: $('#editAnimeTitle').val(),
            synopsis: $('#editAnimeSynopsis').val(),
            release_date: $('#editAnimeReleaseDate').val(),
            status: $('#editAnimeStatus').val()
        };

        // Send updated data to the server
        $.ajax({
            type: "PUT",
            url: `/anime/${animeId}`, // Adjust URL to your endpoint for updating anime
            contentType: "application/json",
            data: JSON.stringify(updatedAnimeData),
            success: function () {
                $('#editAnimeModal').modal('hide'); // Close the modal
                fetchAnime(); // Refresh the anime list
                notifications.show('Anime updated successfully!', 'success');
            },
            error: function (error) {
                console.error('Error updating anime:', error);
                notifications.show('Failed to update anime.', 'error');
            }
        });
    });

    $(document).on('click', '.delete-anime', function () {
        const animeId = $(this).data('id');
        if (confirm(`Are you sure you want to delete anime with ID: ${animeId}?`)) {
            $.ajax({
                type: "DELETE",
                url: `/anime/${animeId}`,
                success: function () {
                    notifications.show('Anime deleted successfully!', 'success');
                    fetchAnime(); // Refresh the anime list
                },
                error: function (error) {
                    console.error('Error deleting anime:', error);
                    notifications.show('Failed to delete anime.', 'error');
                }
            });
        }
    });

    // Add new anime
    $('#submitAnimeButton').on('click', function () {
        const formData = new FormData(); // Use FormData to handle both text and file inputs

        // Append text fields to form data
        formData.append('title', $('#animeTitle').val());
        formData.append('synopsis', $('#animeSynopsis').val());
        formData.append('release_date', $('#animeReleaseDate').val());
        formData.append('status', $('#animeStatus').val());

        // Append files to form data if selected
        const thumbnailFile = $('#animeThumbnail')[0].files[0];
        const bannerFile = $('#animeBanner')[0].files[0];

        if (thumbnailFile) {
            formData.append('thumbnail', thumbnailFile); // Append the thumbnail file
        }
        if (bannerFile) {
            formData.append('banner', bannerFile); // Append the banner file
        }

        $.ajax({
            type: "POST",
            url: "/anime",
            processData: false, // Prevent jQuery from processing the data
            contentType: false, // Set content type to false for FormData
            data: formData,
            success: function () {
                $('#addAnimeModal').modal('hide'); // Close the modal
                notifications.show('Anime added successfully!', 'success');
                $('#animeTitle').val("")
                $('#animeSynopsis').val("")
                $('#animeReleaseDate').val("")
                $('#animeStatus').val("")
                $('#animeThumbnail').val("")
                $('#animeBanner').val("")

                fetchAnime(); // Refresh the anime list
            },
            error: function (error) {
                console.error('Error adding anime:', error);
                notifications.show('Failed to add anime.', 'error');
            }
        });
    });

    // Genre functions
    function fetchGenres() {
        $.ajax({
            type: "GET",
            url: "/genres", // Adjust URL to your endpoint
            success: function (response) {
                $('#genreTableBody').empty();
                response.forEach(function (genre) {
                    const newRow = `
                        <tr>
                            <td>${genre.genre_id}</td>
                            <td>${genre.name}</td>
                            <td>
                                <button class="btn btn-warning btn-sm edit-genre" data-id="${genre.genre_id}">Edit</button>
                                <button class="btn btn-danger btn-sm delete-genre" data-id="${genre.genre_id}">Delete</button>
                            </td>
                        </tr>`;
                    $('#genreTableBody').append(newRow);
                });
            },
            error: function (error) {
                console.error('Error fetching genres:', error);
                notifications.show('Failed to fetch genres list.', 'error');
            }
        });
    }

    $(document).on('click', '.edit-genre', function () {
        const genreId = $(this).data('id');

        // Fetch genre details and open edit modal
        $.ajax({
            type: "GET",
            url: `/genres/${genreId}`, // Adjust URL to your endpoint for fetching genre details
            success: function (genre) {
                $('#editGenreId').val(genre.genre_id); // Hidden input for genre ID
                $('#editGenreName').val(genre.name);

                // Show the edit modal
                $('#editGenreModal').modal('show');
            },
            error: function (error) {
                console.error('Error fetching genre details:', error);
                notifications.show('Failed to fetch genre details.', 'error');
            }
        });
    });

    // Handle saving changes in the edit genre modal
    $('#saveEditGenreButton').on('click', function () {
        const genreId = $('#editGenreId').val(); // Get genre ID from hidden input
        const updatedGenreData = {
            name: $('#editGenreName').val()
        };

        // Send updated data to the server
        $.ajax({
            type: "PUT",
            url: `/genres/${genreId}`, // Adjust URL to your endpoint for updating genre
            contentType: "application/json",
            data: JSON.stringify(updatedGenreData),
            success: function () {
                $('#editGenreModal').modal('hide'); // Close the modal
                fetchGenres(); // Refresh the genre list
                notifications.show('Genre updated successfully!', 'success');
            },
            error: function (error) {
                console.error('Error updating genre:', error);
                notifications.show('Failed to update genre.', 'error');
            }
        });
    });

    $(document).on('click', '.delete-genre', function () {
        const genreId = $(this).data('id');
        if (confirm(`Are you sure you want to delete genre with ID: ${genreId}?`)) {
            $.ajax({
                type: "DELETE",
                url: `/genres/${genreId}`,
                success: function () {
                    notifications.show('Genre deleted successfully!', 'success');
                    fetchGenres(); // Refresh the genre list
                },
                error: function (error) {
                    console.error('Error deleting genre:', error);
                    notifications.show('Failed to delete genre.', 'error');
                }
            });
        }
    });

    // Add new genre
    $('#submitGenreButton').on('click', function () {
        const newGenreData = {
            name: $('#genreName').val()
        };

        $.ajax({
            type: "POST",
            url: "/genres",
            contentType: "application/json",
            data: JSON.stringify(newGenreData),
            success: function () {
                $('#addGenreModal').modal('hide'); // Close the modal
                notifications.show('Genre added successfully!', 'success');
                fetchGenres(); // Refresh the genre list
            },
            error: function (error) {
                console.error('Error adding genre:', error);
                notifications.show('Failed to add genre.', 'error');
            }
        });
    });

    // Episode functions
    //fetching anime for episodes
    function fetchAnimeForEpisode() {
        $.ajax({
            type: "GET",
            url: "/anime", // Adjust URL to your endpoint
            success: function (response) {
                $('#episodeTableBody').empty();
                response.forEach(function (anime) {
                    const newRow = `
                        <tr>
                            <td>${anime.anime_id}</td>
                            <td>${anime.title}</td>
                            <td>${anime.status}</td>
                            <td>${anime.release_date}</td>
                            <td><a style="color:white" href="${anime.thumbnail_url}" target="_blank">View</a></td>
                            <td><a style="color:white" href="${anime.banner_url}" target="_blank">View</a></td>
                            <td>
                                <button style="color:white" class="btn btn-info btn-sm" data-id="${anime.anime_id}" data-bs-toggle="modal" data-bs-target="#editEpisodeModal">Add New Episode</button>
                                <button style="color:white" class="btn btn-info btn-sm" data-id="${anime.anime_id}" data-bs-toggle="modal" data-bs-target="#viewEpisodeModal">View Episodes</button>
                            </td>
                        </tr>`;
                    $('#episodeTableBody').append(newRow);
                });
            },
            error: function (error) {
                console.error('Error fetching anime:', error);
                notifications.show('Failed to fetch anime list.', 'error');
            }
        });
    }


    $(document).on('click', '.btn-info[data-bs-target="#viewEpisodeModal"]', function () {
        var animeId = $(this).data('id'); // Get the anime_id from data attribute
        const requestUrl = `episodes/anime/${animeId}`;
        // console.log(requestUrl)
        // AJAX request to fetch episodes for the selected anime
        $.ajax({
            type: "GET",
            url: requestUrl, // Adjust the URL according to your endpoint
            success: function (response) {
                $('#viewEpisodeTable').html(""); // Clear previous episodes
                response.forEach(function (episode) {
                    // console.log(response)
                    const newRow = `
                        <tr>
                            <td>${episode.episode_id || 'N/A'}</td>
                            <td>${episode.title || 'Unknown Title'}</td>
                            <td>${episode.episode_number || 'N/A'}</td>
                            <td>${episode.status || 'Unknown Status'}</td>
                            <td>
                                <a style="color:white" href="${episode.m3u8_url || '#'}" target="_blank">
                                    Watch
                                </a>
                            </td>
                        </tr>`;
                    $('#viewEpisodeTable').append(newRow); // Append new row to the table
                });
                $('#viewEpisodeModal').modal('show'); // Show the modal
            },
            error: function (xhr) {
                console.error('Error fetching episodes:', xhr);
                notifications.show('Failed to fetch episodes. Please try again later.', 'error');
            }
        });
    });



    //append data to the button 
    $(document).on('click', '.btn-info[data-bs-target="#editEpisodeModal"]', function () {
        const animeId = $(this).data('id');
        $('#saveEpisodeButton').data('anime-id', animeId); // Store anime_id on #saveEpisodeButton
    });

    // Add new episode
    $('#saveEpisodeButton').on('click', function () {
        console.log("Herererere")
        const formData = new FormData();
        const animeId = $(this).data('anime-id'); // Retrieve stored anime_id

        // Append data to formData
        formData.append('anime_id', animeId);
        formData.append('title', $('#editEpisodeTitle').val());
        formData.append('episode_number', $('#editEpisodeNumber').val());

        // Append the video file if selected
        const episodeFile = $('#editVideoUrl')[0].files[0];
        if (episodeFile) {
            formData.append('file', episodeFile); // Use 'file' to match the server-side request key
        }

        $.ajax({
            type: "POST",
            url: "/episodes/upload", // Update to match the upload endpoint
            processData: false,
            contentType: false,
            data: formData,
            success: function () {
                $('#editEpisodeModal').modal('hide');
                notifications.show('Episode added successfully!', 'success');
                fetchAnimeForEpisode();
                $("#editEpisodeTitle").val("");
                $("#editEpisodeNumber").val("");
                $("#editVideoUrl").val("");
            },
            error: function (error) {
                console.error('Error adding episode:', error);
                notifications.show('Failed to add episode.', 'error');
            }
        });
    });












    // Fetch the Anime Quote API key from your server
    // $.ajax({
    //     url: "/env/api/config/anime_quote",
    //     method: "GET",
    //     dataType: "json",
    //     success: function (response) {
    //         const animeQuoteKey = response.anime_quote_key;

    //         $.ajax({
    //             url: "https://waifu.it/api/v4/quote",
    //             method: "GET",
    //             headers: {
    //                 "Authorization": animeQuoteKey 
    //             },
    //             success: function (response) {
    //                 $("#animeQuoteHere").html("<q>" + response.quote + "</q>");
    //                 $("#animeAuthorHere").html("<b>~" + response.author + " (" + response.anime + ")</b>");
    //             },
    //             error: function (jqXHR, textStatus, errorThrown) {
    //                 console.error("Error fetching quote:", errorThrown);
    //             }
    //         });
    //     },
    //     error: function () {
    //         console.error("Failed to fetch Anime Quote API key.");
    //     }
    // });


    function fetchNews() {
        $("#loading").show();

        // Fetch news with offset and limit
        $.ajax({
            url: "/fetch-news",
            method: "GET",
            dataType: "xml",
            success: function (response) {

                // Use the response directly as it is already parsed as XML
                $(response).find("item").each(function () {
                    var title = $(this).find("title").text();
                    var description = $(this).find("description").text();
                    var pubDate = $(this).find("pubDate").text();
                    var link = $(this).find("link").text();

                    // Append each news item as a card to the news container
                    $('#newsContainer').append(`
                        <div class="col-md-4 mb-4">
                            <div class="card custom-card">
                                <div class="card-body">
                                    <h5 class="card-title"><b><a href="${link}" target="_blank">${title}</a></b></h5>
                                    <p class="card-text">${description}</p>
                                    <p class="card-text"><small class="text-muted">${pubDate}</small></p>
                                    <a href="${link}" class="btn btn-primary" target="_blank">Read More</a>
                                </div>
                            </div>
                        </div>
                    `);
                });


            },
            error: function () {
                console.error("Failed to load news.");
                $("#loading").hide();
            }
        });
    }


    function fetchSlideshowImages() {
        $.ajax({
            type: "GET",
            url: "/slideshow/",
            success: function (response) {
                const images = response.images;
                $('#imageTableBody').empty(); 
    
                images.forEach(function (image, index) {
                    const newRow = `
                        <tr>
                            <td>${index + 1}</td> 
                            <td>
                                <p>${image.image_url}</p>
                            </td>
                            <td>
                                <a href="${image.image_url}" class="btn btn-info btn-sm view-image" target="_blank" data-url="${image.url}">View</a>
                            </td>
                        </tr>`;
                    $('#imageTableBody').append(newRow);
                });
    
                // Show the modal after populating the images
                $('#imageModal').modal('show');
            },
            error: function (error) {
                console.error('Error fetching slideshow images:', error);
                notifications.show('Failed to fetch slideshow images list.', 'error');
            }
        });
    }
    

    // Save new image
    $('#saveImageButton').on('click', function () {
        const formData = new FormData();

        // Get all selected image files
        const imageFiles = $('#slideshowImages')[0].files;
        if (imageFiles.length > 0) {
            for (let i = 0; i < imageFiles.length; i++) {
                formData.append('images', imageFiles[i]); // Use 'images' to match the server-side request key

            }
        }

        $.ajax({
            type: "POST",
            url: "/slideshow/upload",
            processData: false,
            contentType: false,
            data: formData,
            success: function (response) {
                $('#addImageModal').modal('hide'); // Close the modal after successful upload
                response.responses.forEach((res) => {
                    // console.log(`Uploaded ${res.title}: ${res.image_url}`);
                    notifications.show(`Uploaded ${res.title}: ${res.image_url}`, 'success');

                });

                $("#slideshowImages").val(""); // Clear the file input
            },
            error: function (error) {
                $('#addImageModal').modal('hide');
                console.error('Error uploading images:', error);
                notifications.show('Failed to add images.', 'error');
            }
        });
    });




    // Call the fetch functions to initialize
    fetchAnime();
    fetchGenres();
    fetchAnimeForEpisode();
    fetchNews();
    fetchSlideshowImages();


});
