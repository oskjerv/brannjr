// Function to set a cookie with expiration days
function setCookie(name, value, days) {
    let date = new Date();
    date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
    document.cookie = name + "=" + value + "; expires=" + date.toUTCString() + "; path=/";
  }

  function getCookie(name) {
    let cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      let [key, value] = cookie.trim().split('=');
      if (key === name) return value;
    }
    return "";
  }


  document.addEventListener("DOMContentLoaded", function () {
    const questionIcon = document.getElementById("question-icon");
    const questionTooltip = document.getElementById("question-tooltip");

    const cookieIcon = document.getElementById("cookie-icon");
    const tooltip = document.getElementById("info-tooltip");
    const acceptBtn = document.getElementById("accept-btn");
    const rejectBtn = document.getElementById("reject-btn");

    function updateButtonStyles() {
      let consent = getCookie("cookieConsent");
      acceptBtn.classList.remove("active-choice");
      rejectBtn.classList.remove("active-choice");

      if (consent === "accepted") {
        acceptBtn.classList.add("active-choice");
      } else if (consent === "rejected") {
        rejectBtn.classList.add("active-choice");
      }
    }

    if (!getCookie("cookieConsent")) {
      tooltip.classList.add("active");
    } else {
      updateButtonStyles();
    }

    cookieIcon.addEventListener("click", function (event) {
      event.stopPropagation();
      tooltip.classList.toggle("active");
      questionTooltip.classList.remove("active");
    });

    questionIcon.addEventListener("click", function (event) {
      event.stopPropagation();
      questionTooltip.classList.toggle("active");
      tooltip.classList.remove("active");
    })

    document.addEventListener("click", function () {
      tooltip.classList.remove("active");
      questionTooltip.classList.remove("active");
    });

    tooltip.addEventListener("click", function (event) {
      event.stopPropagation();
    });

    questionTooltip.addEventListener("click", function (event) {
      event.stopPropagation();
    });

    window.acceptCookies = function () {
      setCookie("cookieConsent", "accepted", 90);
      updateButtonStyles();
      tooltip.classList.remove("active");
    };

    window.rejectCookies = function () {
      setCookie("cookieConsent", "rejected", 90);
      updateButtonStyles();
      tooltip.classList.remove("active");
    };

    updateButtonStyles();
  });