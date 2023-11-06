var options = {
    aspectRatio: "16:9",
    controls: true,
    loop: true,
    preload: "metadata",
    playbackRates: [0.25, 0.5, 1, 1.25, 1.5, 2],
    plugins: {
        hotkeys: {
            seekStep: 15
          },
    },
};

const player = videojs('videoPlayer', options, function() {
         this.controlBar.addChild('QualitySelector');
      });
