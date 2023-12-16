const menuItems = document.querySelectorAll(".menu-item");

const messagesContainer = document.querySelector(".messages-container");

const messageSearchBox = document.querySelector("#message-search");
const eachMessage = document.querySelectorAll(".message");

const middleCreatePost = document.querySelector(".middle .create-post");
const middleFeeds = document.querySelector(".feeds");
const middleStudents = document.querySelector(".students-main-container");

//remove active class for all menuitems
const changeActiveItem = () => {
  menuItems.forEach((items) => {
    items.classList.remove("active");
  });
};
/*===============  LEFT BAR active class ==================== */
menuItems.forEach((items) => {
  items.addEventListener("click", () => {
    changeActiveItem();
    items.classList.add("active");
  });
});

/*============= MESSAGE ===============*/

/* MESSAGE SEARCH BOX */
/*const searchMessage = () => {
  const val = messageSearchBox.value.toLowerCase();
  // console.log(val);
  eachMessage.forEach((chat) => {
    let name = chat.querySelector("h5").textContent.toLowerCase();
    if (name.indexOf(val) != -1) {
      chat.style.display = "flex";
    } else {
      chat.style.display = "none";
    }
  });
};

 messageSearchBox.addEventListener("keyup", searchMessage); */

/* ========================================== */

// const likeBtn = document.querySelector(".action-buttons .heart-fill-red");

// console.log(likeBtn);
// var numberOfClicks = 0;
// likeBtn.addEventListener("click", () => {
//   numberOfClicks += 1;
//   likeBtn.style.fill = "red";
//   if (numberOfClicks % 2 == 0) {
//     likeBtn.style.fill = "white";
//     console.log(numberOfClicks);
//   }
// });

/* ===================POST-SECTION======================= */
const createPostContainer = document.querySelector(
  ".middle .create-post-container"
);
const createPostBtn = document.querySelector(".left .create-post-btn");
const postTextArea = document.querySelector(
  ".middle .create-post-container textarea"
);



const postBtn = document.querySelector(
  ".middle .create-post-container #post-btn"
);


createPostBtn.addEventListener("click", () => {
  createPostContainer.classList.remove("not-active");
 
});
postBtn.addEventListener("click", () => {
  createPostContainer.classList.add("not-active");
 
});




