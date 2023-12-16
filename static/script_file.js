const modalContainer = document.querySelector(".middle .file-modal");
const contributBtn = document.querySelector(
  ".middle .search-filter-students button"
);
const closeModal = document.querySelector(
  ".middle .file-modal-control .close-modal"
);
console.log(closeModal);
contributBtn.addEventListener("click", () => {
  modalContainer.classList.add("js-style");
});
closeModal.addEventListener("click", () => {
  modalContainer.classList.remove("js-style");
});