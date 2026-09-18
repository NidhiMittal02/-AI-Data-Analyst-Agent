document.addEventListener('DOMContentLoaded', () => {

    const dropZone =
        document.getElementById('drop-zone');

    const fileInput =
        document.getElementById('file-upload');

    const fileListEl =
        document.getElementById('file-list');

    const analyzeBtn =
        document.getElementById('analyze-btn');

    const promptInput =
        document.getElementById('prompt');

    const outputArea =
        document.getElementById('output-area');

    const copyBtn =
        document.getElementById('copy-btn');

    const btnText =
        analyzeBtn.querySelector('.btn-text');

    const btnIcon =
        analyzeBtn.querySelector('i');

    const loader =
        analyzeBtn.querySelector('.loader-spinner');


    let selectedFiles = [];


    /* =========================================================
       UPLOAD
       ========================================================= */

    dropZone.addEventListener('click', () => {

        fileInput.click();

    });


    fileInput.addEventListener(
        'change',
        handleFiles
    );


    [
        'dragenter',
        'dragover',
        'dragleave',
        'drop'
    ].forEach(eventName => {

        dropZone.addEventListener(
            eventName,
            preventDefaults
        );

    });


    function preventDefaults(e) {

        e.preventDefault();

        e.stopPropagation();

    }


    [
        'dragenter',
        'dragover'
    ].forEach(eventName => {

        dropZone.addEventListener(
            eventName,
            () => {

                dropZone.classList.add(
                    'dragover'
                );

            }
        );

    });


    [
        'dragleave',
        'drop'
    ].forEach(eventName => {

        dropZone.addEventListener(
            eventName,
            () => {

                dropZone.classList.remove(
                    'dragover'
                );

            }
        );

    });


    dropZone.addEventListener(
        'drop',
        (event) => {

            handleFiles({
                target: {
                    files:
                        event.dataTransfer.files
                }
            });

        }
    );


    function handleFiles(event) {

        const newFiles =
            Array.from(
                event.target.files
            );


        selectedFiles = [
            ...selectedFiles,
            ...newFiles
        ];


        updateFileList();


        fileInput.value = '';

    }


    /* =========================================================
       FILE ICON
       ========================================================= */

    function getFileIcon(filename) {

        const extension =
            filename
                .split('.')
                .pop()
                .toLowerCase();


        if (
            [
                'png',
                'jpg',
                'jpeg',
                'gif'
            ].includes(extension)
        ) {

            return 'ph-image';

        }


        if (
            [
                'csv',
                'xlsx',
                'xls'
            ].includes(extension)
        ) {

            return 'ph-file-csv';

        }


        if (
            [
                'txt',
                'md'
            ].includes(extension)
        ) {

            return 'ph-file-text';

        }


        return 'ph-file';

    }


    /* =========================================================
       ESCAPE HTML
       ========================================================= */

    function escapeHtml(value) {

        const div =
            document.createElement('div');

        div.textContent =
            value;

        return div.innerHTML;

    }


    /* =========================================================
       FILE LIST
       ========================================================= */

    function updateFileList() {

        fileListEl.innerHTML = '';


        selectedFiles.forEach(
            (file, index) => {

                const element =
                    document.createElement(
                        'div'
                    );


                element.className =
                    'file-item';


                element.innerHTML = `

                    <div class="file-info">

                        <i class="ph ${getFileIcon(file.name)}"></i>

                        <span class="file-name">
                            ${escapeHtml(file.name)}
                        </span>

                    </div>


                    <button
                        class="file-remove"
                        type="button"
                        onclick="window.removeSelectedFile(${index})"
                    >

                        <i class="ph ph-x"></i>

                    </button>

                `;


                fileListEl.appendChild(
                    element
                );

            }
        );

    }


    function removeFile(index) {

        selectedFiles.splice(
            index,
            1
        );


        updateFileList();

    }


    window.removeSelectedFile =
        removeFile;


    /* =========================================================
       COPY
       ========================================================= */

    copyBtn.addEventListener(
        'click',
        async () => {

            const text =
                outputArea.dataset.resultText || '';


            if (!text) {

                return;

            }


            try {

                await navigator.clipboard.writeText(
                    text
                );


                const icon =
                    copyBtn.querySelector('i');


                icon.className =
                    'ph ph-check';


                icon.style.color =
                    'var(--success)';


                setTimeout(() => {

                    icon.className =
                        'ph ph-copy';

                    icon.style.color =
                        '';

                }, 2000);


            } catch (error) {

                console.error(
                    'Copy failed:',
                    error
                );

            }

        }
    );


    /* =========================================================
       DISPLAY RESULT
       ========================================================= */

    function displayAnalysisResult(
        responseText
    ) {

        let text =
            responseText.trim();


        /*
         * Remove Markdown code fences
         * if the backend returns them.
         */

        if (
            text.startsWith('```json')
            &&
            text.endsWith('```')
        ) {

            text =
                text
                    .slice(7, -3)
                    .trim();

        }

        else if (
            text.startsWith('```')
            &&
            text.endsWith('```')
        ) {

            text =
                text
                    .slice(3, -3)
                    .trim();

        }


        /* =====================================================
           FIND CHART PATH
           ===================================================== */

        let resultText =
            text;

        let chartPath =
            null;


        const chartMarker =
            'Chart:';


        const chartIndex =
            text.indexOf(
                chartMarker
            );


        if (chartIndex !== -1) {

            resultText =
                text
                    .substring(
                        0,
                        chartIndex
                    )
                    .trim();


            chartPath =
                text
                    .substring(
                        chartIndex +
                        chartMarker.length
                    )
                    .trim();

        }


        /* =====================================================
           SAVE TEXT FOR COPY
           ===================================================== */

        outputArea.dataset.resultText =
            resultText;


        /* =====================================================
           CLEAR OUTPUT
           ===================================================== */

        outputArea.innerHTML =
            '';


        /* =====================================================
           RESULT CARD
           ===================================================== */

        const resultCard =
            document.createElement(
                'div'
            );


        resultCard.className =
            'analysis-result';


        const resultElement =
            document.createElement(
                'pre'
            );


        resultElement.className =
            'analysis-text';


        resultElement.textContent =
            resultText;


        resultCard.appendChild(
            resultElement
        );


        outputArea.appendChild(
            resultCard
        );


        /* =====================================================
           CHART
           ===================================================== */

        if (chartPath) {

            createChart(
                chartPath
            );

        }

    }


    /* =========================================================
       CREATE CHART
       ========================================================= */

    function createChart(
        chartPath
    ) {

        const chartContainer =
            document.createElement(
                'div'
            );


        chartContainer.className =
            'chart-container';


        const title =
            document.createElement(
                'h3'
            );


        title.innerHTML = `

            <i class="ph ph-chart-bar"></i>

            <span>
                Visualization
            </span>

        `;


        chartContainer.appendChild(
            title
        );


        const imageWrapper =
            document.createElement(
                'div'
            );


        imageWrapper.className =
            'chart-image-wrapper';


        const image =
            document.createElement(
                'img'
            );


        image.id =
            'analysis-chart';


        image.alt =
            'Analysis visualization';


        let imageUrl =
            chartPath.trim();


        /*
         * Convert:
         *
         * static/charts/file.png
         *
         * to:
         *
         * /static/charts/file.png
         */

        if (
            imageUrl.startsWith(
                'static/'
            )
        ) {

            imageUrl =
                '/' + imageUrl;

        }


        /*
         * Prevent browser caching.
         */

        imageUrl +=
            '?t=' +
            Date.now();


        image.src =
            imageUrl;


        image.onload =
            () => {

                console.log(
                    'Chart loaded:',
                    imageUrl
                );

            };


        image.onerror =
            () => {

                console.error(
                    'Chart could not load:',
                    imageUrl
                );


                imageWrapper.innerHTML = `

                    <div class="chart-error">

                        <i class="ph ph-warning-circle"></i>

                        <p>
                            Unable to load the chart.
                        </p>

                        <small>
                            ${escapeHtml(imageUrl)}
                        </small>

                    </div>

                `;

            };


        imageWrapper.appendChild(
            image
        );


        chartContainer.appendChild(
            imageWrapper
        );


        outputArea.appendChild(
            chartContainer
        );

    }


    /* =========================================================
       RUN ANALYSIS
       ========================================================= */

    analyzeBtn.addEventListener(
        'click',
        async () => {


            /* -------------------------------------------------
               VALIDATION
               ------------------------------------------------- */

            if (
                !promptInput.value.trim()
                &&
                selectedFiles.length === 0
            ) {

                alert(
                    'Please provide a prompt or upload files to analyze.'
                );

                return;

            }


            /* -------------------------------------------------
               FORM DATA
               ------------------------------------------------- */

            const formData =
                new FormData();


            formData.append(
                'prompt',
                promptInput.value
            );


            selectedFiles.forEach(
                file => {

                    formData.append(
                        file.name,
                        file
                    );

                }
            );


            /* -------------------------------------------------
               LOADING
               ------------------------------------------------- */

            analyzeBtn.disabled =
                true;


            btnText.textContent =
                'Analyzing...';


            btnIcon.style.display =
                'none';


            loader.style.display =
                'block';


            outputArea.dataset.resultText =
                '';


            outputArea.innerHTML = `

                <div class="analysis-loading">

                    <div
                        class="loader-spinner large"
                    ></div>

                    <p>
                        Running AI analysis...
                    </p>

                    <span>
                        Calculating results and generating visualization
                    </span>

                </div>

            `;


            /* -------------------------------------------------
               REQUEST
               ------------------------------------------------- */

            try {

                const response =
                    await fetch(
                        '/analyze',
                        {
                            method: 'POST',
                            body: formData
                        }
                    );


                const responseText =
                    await response.text();


                console.log(
                    'Backend response:',
                    responseText
                );


                /* -------------------------------------------------
                   ERROR
                   ------------------------------------------------- */

                if (!response.ok) {

                    let errorMessage =
                        responseText;


                    try {

                        const errorData =
                            JSON.parse(
                                responseText
                            );


                        if (
                            errorData.error
                        ) {

                            errorMessage =
                                errorData.error;

                        }

                    } catch (error) {

                        // Keep original response.

                    }


                    throw new Error(
                        errorMessage
                    );

                }


                /* -------------------------------------------------
                   SHOW RESULT
                   ------------------------------------------------- */

                displayAnalysisResult(
                    responseText
                );


            } catch (error) {

                console.error(
                    'Analysis error:',
                    error
                );


                outputArea.innerHTML = `

                    <div class="analysis-error">

                        <i class="ph ph-warning-circle"></i>

                        <h3>
                            Analysis failed
                        </h3>

                        <p>
                            ${escapeHtml(error.message)}
                        </p>

                    </div>

                `;

            }


            /* -------------------------------------------------
               RESET BUTTON
               ------------------------------------------------- */

            finally {

                analyzeBtn.disabled =
                    false;


                btnText.textContent =
                    'Run Analysis';


                btnIcon.style.display =
                    'block';


                loader.style.display =
                    'none';

            }

        }
    );

});