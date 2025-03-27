// Document elements
const elements = {
  imageInput: document.getElementById("images"),
  imagePreview: document.getElementById("imagePreview"),
  uploadForm: document.getElementById("uploadForm"),
  result: document.getElementById("result"),
  description: document.getElementById("description"),
  languagesSelect: document.getElementById("languages"),
  preferredLanguagesSelect: document.getElementById("preferredLanguages"),
  preferredStyleSelect: document.getElementById("preferredStyle"),
  styleSelect: document.getElementById("style"),
  settingsPanel: document.getElementById("settingsPanel"),
  themeToggle: document.querySelector(".theme-toggle i"),
  uploadArea: document.getElementById("uploadArea"),
};

// State management
const state = {
  currentMode: "batch",
  selectedFiles: [], // Add this to track all selected files
};

// Theme management
function loadTheme() {
  const theme = localStorage.getItem("theme") || "light";
  document.body.setAttribute("data-theme", theme);
  updateThemeIcon(theme);
}

function toggleTheme() {
  const currentTheme = document.body.getAttribute("data-theme");
  const newTheme = currentTheme === "light" ? "dark" : "light";
  document.body.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  updateThemeIcon(newTheme);
}

function updateThemeIcon(theme) {
  elements.themeToggle.className =
    theme === "light" ? "fas fa-moon" : "fas fa-sun";
}

// Settings management
function loadSettings() {
  const savedLanguages = localStorage.getItem("preferredLanguages");
  if (savedLanguages) {
    const languages = JSON.parse(savedLanguages);
    Array.from(elements.preferredLanguagesSelect.options).forEach((option) => {
      option.selected = languages.includes(option.value);
    });
    Array.from(elements.languagesSelect.options).forEach((option) => {
      option.selected = languages.includes(option.value);
    });
  } else {
    // Default to English
    Array.from(elements.preferredLanguagesSelect.options).forEach((option) => {
      option.selected = option.value === "en";
    });
    Array.from(elements.languagesSelect.options).forEach((option) => {
      option.selected = option.value === "en";
    });
  }

  const savedStyle = localStorage.getItem("preferredStyle");
  if (savedStyle) {
    elements.preferredStyleSelect.value = savedStyle;
    elements.styleSelect.value = savedStyle;
  }
}

function saveSettings() {
  const selectedLanguages = Array.from(
    elements.preferredLanguagesSelect.selectedOptions
  ).map((option) => option.value);
  localStorage.setItem("preferredLanguages", JSON.stringify(selectedLanguages));
  Array.from(elements.languagesSelect.options).forEach((option) => {
    option.selected = selectedLanguages.includes(option.value);
  });

  const selectedStyle = elements.preferredStyleSelect.value;
  localStorage.setItem("preferredStyle", selectedStyle);
  elements.styleSelect.value = selectedStyle;

  toggleSettings();
  showToast("Settings saved successfully!");
}

function toggleSettings() {
  elements.settingsPanel.classList.toggle("open");
}

// UI Utilities
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast-notification";
  toast.textContent = message;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("show");
    setTimeout(() => {
      toast.classList.remove("show");
      setTimeout(() => {
        document.body.removeChild(toast);
      }, 300);
    }, 2000);
  }, 100);
}

function toggleNavbar() {
  document.getElementById("navbarMenu").classList.toggle("show");
}

function setActiveNavLink() {
  const currentPath = window.location.pathname;
  document.querySelectorAll(".nav-link").forEach((link) => {
    link.classList.remove("active");
    if (
      link.getAttribute("href") === currentPath ||
      (currentPath === "/" && link.getAttribute("href") === "/")
    ) {
      link.classList.add("active");
    }
  });
}

// Image handling
function updateImagePreviewLayout() {
  const previewEl = elements.imagePreview;
  const containers = previewEl.querySelectorAll(".image-preview-container");

  if (state.currentMode === "single") {
    previewEl.style.opacity = "0.8";
    setTimeout(() => {
      previewEl.classList.add("single-mode");
      previewEl.style.opacity = "1";

      containers.forEach((container, index) => {
        setTimeout(() => {
          container.classList.add("single-item");

          if (!container.querySelector(".item-number")) {
            const itemLabel = document.createElement("span");
            itemLabel.className = "item-number";
            itemLabel.textContent = `#${index + 1}`;
            container.appendChild(itemLabel);
          }

          if (!container.querySelector(".item-measurements")) {
            const measurementField = document.createElement("div");
            measurementField.className = "item-measurements mt-2";
            measurementField.innerHTML = `
              <textarea 
                class="form-control form-control-sm" 
                id="measurements-item-${index}" 
                placeholder="Measurements for item #${index + 1}" 
                rows="2"
              ></textarea>
            `;
            container.appendChild(measurementField);
          }
        }, index * 70);
      });
    }, 200);
  } else {
    previewEl.style.opacity = "0.8";
    setTimeout(() => {
      previewEl.classList.remove("single-mode");
      previewEl.style.opacity = "1";

      containers.forEach((container, index) => {
        setTimeout(() => {
          container.classList.remove("single-item");
          const itemElements = container.querySelectorAll(
            ".item-number, .item-measurements"
          );
          itemElements.forEach((el) => el.remove());
        }, index * 40);
      });
    }, 200);
  }
}

function handleImagePreview() {
  const newFiles = Array.from(elements.imageInput.files || []);

  if (newFiles.length === 0) {
    return;
  }

  // Add the new files to our tracked collection
  const combinedFiles = [...state.selectedFiles, ...newFiles];

  // Check if we would exceed the limit
  if (combinedFiles.length > 10) {
    showToast(
      "You can upload up to 10 images only. Please remove some images first."
    );
    elements.imageInput.value = "";
    return;
  }

  // Update our state with the combined files
  state.selectedFiles = combinedFiles;

  // Reset the file input so the same files can be selected again if needed
  elements.imageInput.value = "";

  // Refresh the UI
  refreshImagePreview();
}

// New function to separate UI refresh from file handling
function refreshImagePreview() {
  // Clear the preview area
  elements.imagePreview.innerHTML = "";

  if (state.selectedFiles.length === 0) {
    elements.imagePreview.style.display = "none";
    return;
  }

  elements.imagePreview.style.display = "flex";

  // Add the clear all button if needed
  if (state.selectedFiles.length > 1) {
    addClearAllButton();
  }

  let loadedImages = 0;
  const totalImagesToLoad = state.selectedFiles.filter((file) =>
    file.type.startsWith("image/")
  ).length;

  // Create preview elements for each file
  state.selectedFiles.forEach((file, index) => {
    if (file.type.startsWith("image/")) {
      const reader = new FileReader();

      reader.onload = (e) => {
        const container = document.createElement("div");
        container.className = "image-preview-container";
        // Store the array index for deletion reference
        container.dataset.index = index;

        const img = document.createElement("img");
        img.src = e.target.result;
        img.className = "preview-image";
        img.alt = file.name;

        const removeBtn = document.createElement("button");
        removeBtn.className = "remove-image";
        removeBtn.innerHTML = "×";
        // Use a closure to capture the current index
        removeBtn.onclick = function (event) {
          event.preventDefault();
          event.stopPropagation();
          // Use the file itself as the identifier instead of index
          removeImage(file);
        };

        container.appendChild(img);
        container.appendChild(removeBtn);
        elements.imagePreview.appendChild(container);

        loadedImages++;
        if (loadedImages === totalImagesToLoad) {
          updateImagePreviewLayout();
        }
      };

      reader.readAsDataURL(file);
    }
  });
}

// Updated removeImage to use the file object as identifier
function removeImage(fileToRemove) {
  try {
    // Remove the file from our array
    state.selectedFiles = state.selectedFiles.filter(
      (file) => file !== fileToRemove
    );

    // Refresh the UI
    refreshImagePreview();

    // Show feedback
    if (state.selectedFiles.length === 0) {
      showToast("All images removed");
    } else {
      showToast("Image removed");
    }
  } catch (error) {
    console.error("Error removing image:", error);
    showToast("Error removing image");
  }
}

function addClearAllButton() {
  // Remove existing clear all button if it exists
  const existingBtn = elements.imagePreview.querySelector(".clear-all-images");
  if (existingBtn) existingBtn.remove();

  const clearAllBtn = document.createElement("button");
  clearAllBtn.className = "clear-all-images";
  clearAllBtn.innerHTML = "<i class='fas fa-trash'></i> Clear All";
  clearAllBtn.onclick = function (event) {
    event.preventDefault();
    try {
      // Clear the array
      state.selectedFiles = [];

      // Refresh the UI
      refreshImagePreview();

      // Show feedback
      showToast("All images cleared");
    } catch (error) {
      console.error("Error clearing images:", error);
      showToast("Error clearing images");
    }
  };

  elements.imagePreview.prepend(clearAllBtn);
}

// Drag and drop handling
function setupDragAndDrop() {
  elements.uploadArea.addEventListener("dragover", (e) => {
    e.preventDefault();
    elements.uploadArea.classList.add("dragover");
  });

  elements.uploadArea.addEventListener("dragleave", () => {
    elements.uploadArea.classList.remove("dragover");
  });

  elements.uploadArea.addEventListener("drop", (e) => {
    e.preventDefault();
    elements.uploadArea.classList.remove("dragover");

    if (e.dataTransfer.files.length > 10) {
      showToast("You can upload up to 10 images only.");
      return;
    }

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      const dt = new DataTransfer();
      Array.from(e.dataTransfer.files).forEach((file) => {
        dt.items.add(file);
      });
      elements.imageInput.files = dt.files;
      handleImagePreview();
    }
  });
}

// Form submission
async function handleFormSubmit(e) {
  // Make sure to prevent default form submission behavior right away
  e.preventDefault();
  console.log("Form submission intercepted");

  try {
    if (state.selectedFiles.length === 0) {
      showToast("Please select at least one image");
      return;
    }

    const selectedLanguages = Array.from(
      elements.languagesSelect.selectedOptions
    ).map((option) => option.value);

    if (selectedLanguages.length === 0) {
      showToast("Please select at least one language");
      return;
    }

    // Loading state
    elements.uploadForm.classList.add("loading");
    const submitButton = elements.uploadForm.querySelector(
      'button[type="submit"]'
    );
    submitButton.disabled = true;
    submitButton.innerHTML = "Generating...";

    if (state.currentMode === "batch") {
      await processBatchUpload(state.selectedFiles, selectedLanguages);
    } else {
      await processSingleUpload(state.selectedFiles, selectedLanguages);
    }

    // Remove loading state
    elements.uploadForm.classList.remove("loading");
    submitButton.disabled = false;
    submitButton.innerHTML = "Generate Description";
  } catch (error) {
    console.error("Error during form submission:", error);
    showToast("Error processing request. Check console for details.");

    // Reset the form state
    elements.uploadForm.classList.remove("loading");
    const submitButton = elements.uploadForm.querySelector(
      'button[type="submit"]'
    );
    if (submitButton) {
      submitButton.disabled = false;
      submitButton.innerHTML = "Generate Description";
    }
  }
}

// Modify processBatchUpload to add better error handling
async function processBatchUpload(files, selectedLanguages) {
  try {
    const formData = new FormData();

    console.log(`Processing ${files.length} files for upload`);

    // Add each file to the form data
    for (let i = 0; i < files.length; i++) {
      formData.append("images", files[i]);
    }

    // Add the other form fields
    formData.append(
      "measurements",
      document.getElementById("measurements").value
    );
    formData.append("style", document.getElementById("style").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("languages", JSON.stringify(selectedLanguages));

    console.log("Sending request to backend");

    // Send the request to the backend
    const response = await fetch("/generate", {
      method: "POST",
      body: formData,
    });

    console.log("Backend response received:", response.status);

    if (!response.ok) {
      const errorText = await response.text();
      console.error("Server responded with error:", response.status, errorText);
      showToast(
        `Server error: ${response.status} - ${errorText || "Unknown error"}`
      );
      return;
    }

    const data = await response.json();
    console.log("Response parsed successfully");

    // Update the UI with the generated description
    elements.result.innerHTML = `
      <h3>Generated Description</h3>
      <div class="card">
        <div class="card-body">
          <div id="description" class="card-text">${data.description}</div>
          <div class="copy-btn-wrapper">
            <button class="btn-copy" onclick="copyToClipboard()">
              <i class="fas fa-clipboard"></i> Copy to Clipboard
            </button>
          </div>
        </div>
      </div>
    `;

    elements.description = document.getElementById("description");
    elements.result.style.display = "block";
    elements.result.classList.remove("show");

    setTimeout(() => {
      elements.result.classList.add("show");
    }, 50);

    showToast("Description generated successfully!");
  } catch (error) {
    console.error("Error in processBatchUpload:", error);
    showToast("Error generating description. Please try again.");
  }
}

async function processSingleUpload(files, selectedLanguages) {
  elements.result.innerHTML = `
    <h3>Generated Descriptions</h3>
    <div class="card">
      <div class="card-body">
        <div id="description"></div>
      </div>
    </div>
  `;

  elements.description = document.getElementById("description");
  elements.result.style.display = "block";
  elements.result.classList.remove("show");

  let successCount = 0;

  for (let i = 0; i < files.length; i++) {
    const formData = new FormData();
    formData.append("images", files[i]);

    if (state.currentMode === "single") {
      const itemMeasurement = document.getElementById(`measurements-item-${i}`);
      formData.append(
        "measurements",
        itemMeasurement ? itemMeasurement.value : ""
      );
    } else {
      formData.append(
        "measurements",
        document.getElementById("measurements").value
      );
    }

    formData.append("style", document.getElementById("style").value);
    formData.append("category", document.getElementById("category").value);
    formData.append("languages", JSON.stringify(selectedLanguages));

    try {
      const response = await fetch("/generate", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (response.ok) {
        const itemDesc = document.createElement("div");
        itemDesc.className = "item-description mb-4";

        if (i > 0) {
          const separator = document.createElement("hr");
          itemDesc.appendChild(separator);
        }

        const itemTitle = document.createElement("h4");
        itemTitle.className = "item-title";
        itemTitle.textContent = `Item ${i + 1}`;
        itemDesc.appendChild(itemTitle);

        const descText = document.createElement("div");
        descText.className = "description-text";
        descText.textContent = data.description;
        itemDesc.appendChild(descText);

        const copyBtnWrapper = document.createElement("div");
        copyBtnWrapper.className = "copy-btn-wrapper";

        const copyBtn = document.createElement("button");
        copyBtn.className = "btn-copy btn-copy-item";
        copyBtn.innerHTML = '<i class="fas fa-clipboard"></i> Copy This Item';
        copyBtn.onclick = function () {
          copyItemToClipboard(data.description, copyBtn);
        };

        copyBtnWrapper.appendChild(copyBtn);
        itemDesc.appendChild(copyBtnWrapper);
        elements.description.appendChild(itemDesc);
        successCount++;
      }
    } catch (error) {
      console.error(`Error for item ${i + 1}:`, error);
    }
  }

  if (successCount > 1) {
    const copyAllWrapper = document.createElement("div");
    copyAllWrapper.className = "copy-btn-wrapper copy-all-wrapper";

    const copyAllBtn = document.createElement("button");
    copyAllBtn.className = "btn-copy btn-copy-all";
    copyAllBtn.innerHTML = '<i class="fas fa-copy"></i> Copy All Descriptions';
    copyAllBtn.onclick = copyToClipboard;

    copyAllWrapper.appendChild(copyAllBtn);
    elements.description.appendChild(copyAllWrapper);
  }

  setTimeout(() => {
    elements.result.classList.add("show");
  }, 50);

  showToast(`Generated ${successCount} of ${files.length} descriptions!`);
}

// Clipboard functions
function copyItemToClipboard(text, buttonElement) {
  navigator.clipboard
    .writeText(text)
    .then(() => {
      buttonElement.classList.add("copy-success");
      buttonElement.innerHTML = '<i class="fas fa-check"></i> Copied!';

      setTimeout(() => {
        buttonElement.classList.remove("copy-success");
        buttonElement.innerHTML =
          '<i class="fas fa-clipboard"></i> Copy This Item';
      }, 2000);

      showToast("Item description copied to clipboard!");
    })
    .catch((err) => {
      console.error("Failed to copy: ", err);
      showToast("Failed to copy to clipboard.");
    });
}

function copyToClipboard() {
  const text = elements.description.textContent;
  navigator.clipboard
    .writeText(text)
    .then(() => {
      const copyBtn = document.querySelector(".btn-copy");
      copyBtn.classList.add("copy-success");
      copyBtn.innerHTML = '<i class="fas fa-check"></i> Copied!';

      setTimeout(() => {
        copyBtn.classList.remove("copy-success");
        copyBtn.innerHTML =
          '<i class="fas fa-clipboard"></i> Copy to Clipboard';
      }, 2000);

      showToast("Description copied to clipboard!");
    })
    .catch((err) => {
      console.error("Failed to copy: ", err);
      showToast("Failed to copy to clipboard.");
    });
}

// Event listeners
function setupEventListeners() {
  // Check if elements exist before attaching
  if (elements.imageInput) {
    elements.imageInput.addEventListener("change", handleImagePreview);
  } else {
    console.error("Image input element not found");
  }

  if (elements.uploadForm) {
    console.log("Attaching submit event listener to form");
    // First, remove any existing listeners to avoid duplication
    elements.uploadForm.removeEventListener("submit", handleFormSubmit);
    // Then add the event listener
    elements.uploadForm.addEventListener("submit", handleFormSubmit);

    // Also attach a click handler to the button as a fallback
    const submitButton = document.getElementById("generateBtn");
    if (submitButton) {
      submitButton.addEventListener("click", function (e) {
        e.preventDefault();
        console.log("Generate button clicked directly");
        handleFormSubmit(new Event("submit"));
      });
    }
  } else {
    console.error("Upload form element not found");
  }

  if (document.getElementById("modeBatch")) {
    document
      .getElementById("modeBatch")
      .addEventListener("change", function () {
        state.currentMode = "batch";
        updateImagePreviewLayout();
      });
  }

  if (document.getElementById("modeSingle")) {
    document
      .getElementById("modeSingle")
      .addEventListener("change", function () {
        state.currentMode = "single";
        updateImagePreviewLayout();
      });
  }
}

// Initialize
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM loaded, initializing app");

  // Re-initialize elements to ensure they're found correctly
  Object.keys(elements).forEach((key) => {
    const selector = elements[key] ? elements[key].id || key : key;
    if (key === "themeToggle") return; // Skip themeToggle as it's a querySelector
    if (key === "uploadArea")
      elements[key] = document.getElementById("uploadArea");
    else if (key === "imageInput")
      elements[key] = document.getElementById("images");
    else elements[key] = document.getElementById(selector);

    if (!elements[key]) {
      console.warn(`Element ${key} not found in DOM`);
    }
  });

  setupEventListeners();
  setupDragAndDrop();
  loadSettings();
  loadTheme();
  setActiveNavLink();
});
