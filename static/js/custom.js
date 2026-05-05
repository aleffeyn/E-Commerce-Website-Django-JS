function sendArticleComment(articleId) {
    var comment = $('#commentText').val();
    var parentId = $('#parent_id').val();

    // Check if comment is empty or whitespace-only
    if (!comment || !comment.trim()) {
        showCommentError('لطفا نظر خود را وارد کنید');
        return;
    }

    // Hide any previous error
    hideCommentError();

    console.log(parentId);
    $.get('/articles/add-article-comment', {
        article_comment: comment.trim(),
        article_id: articleId,
        parent_id: parentId
    }).then(res => {
        $('#comment_area').html(res);
        $('#commentText').val('');
        $('#parent_id').val('');

        if (parentId !== null && parentId !== '') {
            document.getElementById('single_comment_box_' + parentId).scrollIntoView({behavior: "smooth"});
        } else {
            document.getElementById('comment_area').scrollIntoView({behavior: "smooth"});
        }
    }).fail(function (xhr) {
        showCommentError(xhr.responseText || 'خطایی رخ داده است');
    });
}

function showCommentError(message) {
    hideCommentError();

    var errorHtml = '<div id="comment_error" class="alert alert-danger" style="margin-top: 10px;">' +
        '<i class="fa fa-exclamation-circle"></i> ' + message + '</div>';

    $('#commentText').after(errorHtml);

    // Auto-hide after 5 seconds
    setTimeout(function () {
        hideCommentError();
    }, 5000);
}

function hideCommentError() {
    $('#comment_error').remove();
}

function fillParentId(parentId) {
    $('#parent_id').val(parentId);
    document.getElementById('comment_form').scrollIntoView({behavior: "smooth"});
}

// Sync price inputs with slider
$(document).ready(function () {
    // When slider changes, update input fields
    $('#sl2').on('slide', function (ev) {
        var values = ev.value;
        $('#price_min_input').val(values[0]);
        $('#price_max_input').val(values[1]);
    });

    // When input fields change, update slider
    $('#price_min_input, #price_max_input').on('change', function () {
        var minVal = parseInt($('#price_min_input').val()) || 0;
        var maxVal = parseInt($('#price_max_input').val()) || parseInt($('#price_max_input').attr('max'));

        // Ensure min doesn't exceed max
        if (minVal > maxVal) {
            var temp = minVal;
            minVal = maxVal;
            maxVal = temp;
            $('#price_min_input').val(minVal);
            $('#price_max_input').val(maxVal);
        }

        // Update the slider
        $('#sl2').slider('setValue', [minVal, maxVal]);
    });

    // Ensure checkboxes match URL params on page load
    const urlParams = new URLSearchParams(window.location.search);
    const selectedBrands = urlParams.getAll('brands');

    $('.brand-checkbox').each(function () {
        if (selectedBrands.includes($(this).val())) {
            $(this).prop('checked', true);
        }
    });

    initProductGallery();
    initHeaderProductSearch();
});

function initHeaderProductSearch() {
    var searchInput = $('#header-search-input');
    var searchForm = $('#header-search-form');
    var suggestionBox = $('#header-search-suggestions');

    if (!searchInput.length || !searchForm.length || !suggestionBox.length) {
        return;
    }

    var suggestUrl = searchInput.data('suggest-url');
    var debounceTimer = null;

    function hideSuggestions() {
        suggestionBox.empty().hide();
    }

    function renderSuggestions(items) {
        suggestionBox.empty();
        if (!items || !items.length) {
            hideSuggestions();
            return;
        }

        items.forEach(function (item) {
            var li = $('<li></li>');
            var link = $('<a></a>')
                .attr('href', item.url)
                .text(item.title);
            li.append(link);
            suggestionBox.append(li);
        });
        suggestionBox.show();
    }

    searchInput.on('input', function () {
        var query = searchInput.val().trim();
        clearTimeout(debounceTimer);

        if (query.length < 2) {
            hideSuggestions();
            return;
        }

        debounceTimer = setTimeout(function () {
            $.get(suggestUrl, {q: query}).done(function (response) {
                renderSuggestions(response.results || []);
            }).fail(function () {
                hideSuggestions();
            });
        }, 250);
    });

    searchInput.on('keydown', function (event) {
        if (event.key === 'Enter') {
            hideSuggestions();
            searchForm.submit();
        }
    });

    $(document).on('click', function (event) {
        if (!$(event.target).closest('.search_box').length) {
            hideSuggestions();
        }
    });
}

function initProductGallery() {
    var root = document.getElementById('product-gallery');
    if (!root) {
        return;
    }

    var mainImg = document.getElementById('product-gallery-main');
    var zoomBtn = document.getElementById('product-gallery-zoom');
    var lightbox = document.getElementById('pg-lightbox');
    if (!mainImg || !zoomBtn || !lightbox) {
        return;
    }

    var thumbNodes = root.querySelectorAll('.product-gallery__thumb');
    var slides = [];
    var i;
    for (i = 0; i < thumbNodes.length; i++) {
        var btn = thumbNodes[i];
        slides.push({
            full: btn.getAttribute('data-full-src'),
            main: btn.getAttribute('data-main-src'),
            alt: btn.getAttribute('data-alt') || ''
        });
    }
    if (!slides.length) {
        return;
    }

    var lbImg = lightbox.querySelector('.pg-lightbox__img');
    var lbPrev = lightbox.querySelector('.pg-lightbox__nav--prev');
    var lbNext = lightbox.querySelector('.pg-lightbox__nav--next');
    var lbClose = lightbox.querySelector('.pg-lightbox__close');
    var lbBackdrop = lightbox.querySelector('.pg-lightbox__backdrop');

    var activeIndex = 0;
    for (i = 0; i < thumbNodes.length; i++) {
        if (thumbNodes[i].classList.contains('is-active')) {
            activeIndex = i;
            break;
        }
    }

    var lbIndex = activeIndex;

    function setActiveThumb(index) {
        for (i = 0; i < thumbNodes.length; i++) {
            thumbNodes[i].classList.toggle('is-active', i === index);
        }
        activeIndex = index;
    }

    function swapMainImage(index) {
        var s = slides[index];
        if (!s || !s.main) {
            return;
        }

        setActiveThumb(index);

        function applySrc() {
            mainImg.src = s.main;
            mainImg.setAttribute('data-full-src', s.full);
            mainImg.alt = s.alt;
            mainImg.classList.remove('is-animating');
        }

        var reduceMotion = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
        if (reduceMotion) {
            applySrc();
            return;
        }

        mainImg.classList.add('is-animating');
        window.setTimeout(function () {
            var loader = new Image();
            loader.onload = function () {
                applySrc();
            };
            loader.onerror = function () {
                applySrc();
            };
            loader.src = s.main;
            if (loader.complete) {
                applySrc();
            }
        }, 200);
    }

    for (i = 0; i < thumbNodes.length; i++) {
        (function (idx) {
            thumbNodes[idx].addEventListener('click', function () {
                swapMainImage(idx);
            });
        })(i);
    }

    function updateLbNavVisibility() {
        var single = slides.length <= 1;
        if (lbPrev) {
            lbPrev.classList.toggle('is-hidden', single);
        }
        if (lbNext) {
            lbNext.classList.toggle('is-hidden', single);
        }
    }

    function setLightboxImage(index, skipFade) {
        var s = slides[index];
        if (!s || !lbImg) {
            return;
        }
        lbIndex = index;

        function showLoaded() {
            lbImg.classList.add('is-loaded');
        }

        if (skipFade) {
            lbImg.classList.remove('is-loaded');
        } else {
            lbImg.classList.remove('is-loaded');
        }

        var next = new Image();
        next.onload = function () {
            lbImg.src = s.full;
            lbImg.alt = s.alt;
            window.requestAnimationFrame(function () {
                showLoaded();
            });
        };
        next.onerror = function () {
            lbImg.src = s.full;
            lbImg.alt = s.alt;
            showLoaded();
        };
        next.src = s.full;
    }

    function openLightbox() {
        var full = mainImg.getAttribute('data-full-src');
        if (!full) {
            return;
        }
        lbIndex = activeIndex;
        lightbox.removeAttribute('hidden');
        lightbox.setAttribute('aria-hidden', 'false');
        lightbox.classList.add('is-open');
        document.body.style.overflow = 'hidden';
        updateLbNavVisibility();
        lbImg.classList.remove('is-loaded');
        setLightboxImage(lbIndex, true);
    }

    function closeLightbox() {
        lightbox.classList.remove('is-open');
        lightbox.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
        window.setTimeout(function () {
            if (!lightbox.classList.contains('is-open')) {
                lightbox.setAttribute('hidden', '');
            }
        }, 350);
    }

    zoomBtn.addEventListener('click', openLightbox);
    if (lbClose) {
        lbClose.addEventListener('click', closeLightbox);
    }
    if (lbBackdrop) {
        lbBackdrop.addEventListener('click', closeLightbox);
    }

    if (lbPrev) {
        lbPrev.addEventListener('click', function () {
            if (slides.length <= 1) {
                return;
            }
            lbIndex = (lbIndex - 1 + slides.length) % slides.length;
            setLightboxImage(lbIndex, false);
        });
    }
    if (lbNext) {
        lbNext.addEventListener('click', function () {
            if (slides.length <= 1) {
                return;
            }
            lbIndex = (lbIndex + 1) % slides.length;
            setLightboxImage(lbIndex, false);
        });
    }

    document.addEventListener('keydown', function (ev) {
        if (!lightbox.classList.contains('is-open')) {
            return;
        }
        if (ev.key === 'Escape') {
            closeLightbox();
            ev.preventDefault();
        } else if (ev.key === 'ArrowRight' && slides.length > 1) {
            lbIndex = (lbIndex + 1) % slides.length;
            setLightboxImage(lbIndex, false);
            ev.preventDefault();
        } else if (ev.key === 'ArrowLeft' && slides.length > 1) {
            lbIndex = (lbIndex - 1 + slides.length) % slides.length;
            setLightboxImage(lbIndex, false);
            ev.preventDefault();
        }
    });
}

function filterProducts() {
    // Get values from input fields (they're synced with slider)
    var start_price = $('#price_min_input').val() || 0;
    var end_price = $('#price_max_input').val() || $('#price_max_input').attr('max');

    $('#start_price').val(start_price);
    $('#end_price').val(end_price);

    updateBrandsInForm();
    $('#page').val(1);
    $('#filter_form').submit();
}

function fillPage(page) {
    updateBrandsInForm();
    $('#page').val(page);
    $('#filter_form').submit();
}

function updateBrandsInForm() {
    $('#brands_container').empty();
    $('.brand-checkbox:checked').each(function () {
        $('#brands_container').append(
            '<input type="hidden" name="brands" value="' + $(this).val() + '">'
        );
    });
}

function resetFilters() {
    // Reset price inputs to default
    $('#price_min_input').val(0);
    $('#price_max_input').val($('#price_max_input').attr('max'));

    // Reset slider
    var maxPrice = parseInt($('#sl2').attr('data-slider-max')) || 0;
    $('#sl2').slider('setValue', [0, maxPrice]);

    // Clear the hidden inputs
    $('#start_price').val('');
    $('#end_price').val('');
    $('#page').val('1');

    // Uncheck all brand checkboxes
    $('.brand-checkbox').prop('checked', false);
    $('#brands_container').empty();

    $('#filter_form').submit();
}

function addProductToOrder(productId , productSlug) {
    const productCount = $('#product-count').val();
    $.get('/order/add-to-order?product_id=' + productId + '&count=' + productCount).then(res => {
        if (res.status === 'success') {
            Swal.fire({
                title: res.title,
                text: res.message,
                icon: res.icon,
                showCancelButton: true,
                confirmButtonColor: "#0d7905",
                cancelButtonColor: "#172b96",
                confirmButtonText: res.confirm_button_text,
                cancelButtonText: res.cancel_button_text,
            }).then((result) => {
                if (result.isConfirmed) Swal.fire({
                    title: "بزن بریم",
                    text: "در حال انتقال به سبد خرید",
                    icon: "success",
                    timer: 3000,
                    confirmButtonText: "باشه"
                }).then(() => {
                    window.location.href = '/user/user-basket';
                })
            });
        } else {
            Swal.fire({
                title: res.title,
                text: res.message,
                icon: res.icon,
                showCancelButton: false,
                confirmButtonColor: "#3085d6",
                confirmButtonText: res.confirm_button_text
            }).then((result) => {
                if (res.status === 'not_logged_in' && result.isConfirmed) {
                    var currentPath = window.location.pathname + window.location.search + window.location.hash;
                    window.location.href = '/login?next=' + encodeURIComponent(currentPath);
                }
            });
        }
    })
}

function removeProductFromOrder(detailId) {
    Swal.fire({
        title: "حذف محصول از سبد خرید",
        text: "مطمئنی میخوای این محصول رو از سبد خریدت حذف کنی؟",
        icon: "warning",
        showCancelButton: true,
        confirmButtonColor: "#3085d6",
        cancelButtonColor: "#d33",
        confirmButtonText: "اره حذف کن!",
        cancelButtonText: "نه پشیمون شدم",
    }).then((result) => {
        if (!result.isConfirmed) return;

        $.get('/user/remove-order-detail?detail_id=' + detailId).then(res => {
            if (res.status === 'success') {
                $('#order-detail-content').html(res.body);
                Swal.fire({
                    title: "حذف محصول",
                    text: "محصول مورد نظر با موفقیت از سبد خرید شما حذف شد.",
                    icon: "success",
                    confirmButtonText: "باشه"
                });
            } else {
                Swal.fire({
                    title: "ناموجود",
                    text: "این محصول دیگر موجود نیست.",
                    icon: "error",
                    confirmButtonText: "باشه"
                });
            }
        }).fail(() => {
            Swal.fire({
                title: "خطا",
                text: "این محصول دیگر موجود نیست.",
                icon: "error",
                confirmButtonText: "باشه"
            });
        });
    });
}

function changeOrderDetailCount(detailId, state) {
    $.get('/user/change_order_detail?detail_id=' + detailId + '&state=' + state).then(res => {
        if (res.status === 'success'){
            $('#order-detail-content').html(res.body);
        }
    })
}