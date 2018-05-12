Notes
=====

- Containers for this image are run in ephemeral mode. this means that
  one the container is stopped, it is automatically deleted. This is
  possible since we use a shared voulme for the files.
- You should edit your profile to use espeak as the default TTS since
  it's the only free software offline engine available for the moment.
  Installation of svox is not supported because it's proprietary software.
- Once you have defined the profile and resources git links, these will be
  already configured when Kalliope starts. The purpose is to separate
  completely the profile from the other components such as the neurons
  so that the user always works with a clean and more manageable profile.

