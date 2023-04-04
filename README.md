<p align="center">
  <a href="https://www.dontmanagelms.com/">
    <img src="https://www.dontmanagelms.com/files/flms.svg" alt="DontManage LMS" width="100" height="100">
  </a>
  <p align="center">Easy to use, open source, learning management system.</p>
</p>

<p align="center">
  <a href="https://github.com/dontmanage/lms/blob/main/LICENSE">
    <img alt="license" src="https://img.shields.io/badge/license-AGPLv3-blue">
  </a>
</p>

<img width="1402" alt="Lesson" src="https://dontmanagelms.com/files/fs-banner71f330.png">

<details>
	<summary>Show more screenshots</summary>
	<img width="1520" alt="ss1" src="https://user-images.githubusercontent.com/31363128/210056046-584bc8aa-d28c-4514-b031-73817012837d.png">
	<img width="830" alt="ss2" src="https://user-images.githubusercontent.com/31363128/210056097-36849182-6db0-43a2-8c62-5333cd2aedf4.png">
	<img width="941" alt="ss3" src="https://user-images.githubusercontent.com/31363128/210056134-01a7c429-1ef4-434e-9d43-128dda35d7e5.png">
</details>

DontManage LMS is an easy-to-use, open-source learning management system. You can use it to create and share online courses. The app has a clear UI that helps students focus only on what's important and assists in distraction-free learning.

You can create courses and lessons through simple forms. Lessons can be in the form of text, videos, quizzes or a combination of all these. You can keep your students engaged with quizzes to help revise and test the concepts learned. Course Instructors and Students can reach out to each other through the discussions section available for each lesson and get queries resolved.

## Features
- Create online courses. 📚
- Add detailed descriptions and preview videos to the course. 🎬
- Add videos, quizzes, and assignments to your lessons and make them interesting and interactive 📝
- Discussions section below each lesson where instructors and students can interact with each other. 💬
- Create classes to group your students based on courses and track their progress 🏛
- Statistics dashboard that provides all important numbers at a glimpse. 📈
- Job Board where users can post and look for jobs. 💼
- People directory with each person's profile page 👨‍👩‍👧‍👦
- Set cover image, profile photo, short bio, and other professional information. 🦹🏼‍♀️
- Simple layout that optimizes readability 🤓
- Delightful user experience in overall usage ✨

## Tech Stack

DontManage LMS is built on [DontManage Framework](https://dontmanageframework.com) which is a batteries-included python web framework.
These are some of the tools it's built on:
- [Python](https://www.python.org)
- [Redis](https://redis.io/)
- [MariaDB](https://mariadb.org/)
- [Socket.io](https://socket.io/)

## Local Setup

### Docker
You need Docker, docker-compose, and git setup on your machine. Refer to [Docker documentation](https://docs.docker.com/). After that, run the following commands:
```
git clone https://github.com/dontmanage/lms
cd apps/lms/docker
docker-compose up
```

Wait for some time until the setup script creates a site. After that, you can access `http://localhost:8000` in your browser and the app's login screen should show up.

### DontManage Bench

Currently, this app depends on the `develop` branch of [dontmanage](https://github.com/dontmanage/dontmanage).

1. Setup dontmanage-bench by following [this guide](https://dontmanageframework.com/docs/v14/user/en/installation)
1. In the dontmanage-bench directory, run `bench start` and keep it running. Open a new terminal session and cd into the `dontmanage-bench` directory.
1. Run the following commands:
    ```sh
    bench new-site lms.test
    bench get-app lms
    bench --site lms.test install-app lms
    bench --site lms.test add-to-hosts

 1. Now, you can access the site at `http://lms.test:8000`


## Deployment
DontManage LMS is an app built on top of the DontManage Framework. So, you can follow any deployment guide for hosting a DontManage Framework-based site.

### Managed Hosting
DontManage LMS can be deployed in a few clicks on [DontManage Cloud](https://dontmanagecloud.com/marketplace/apps/lms).

### Self-hosting
If you want to self-host, you can follow official [DontManage Bench Installation](https://github.com/dontmanage/bench#installation) instructions.

## Bugs and Feature Requests
If you find any bugs or have a feature idea for the app, feel free to report them here on [GitHub Issues](https://github.com/dontmanage/lms/issues). Make sure you share enough information (app screenshots, browser console screenshots, stack traces, etc) for project maintainers.

## License
Distributed under [GNU AFFERO GENERAL PUBLIC LICENSE](license.txt)
