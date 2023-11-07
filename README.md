# TasteVideo 短视频应用

欢迎来到TasteVideo，这是一个使用Vue3、Tailwind CSS和Python FastAPI构建的网页短视频应用。我们的应用提供流畅的视频播放体验，并且拥有丰富的视频内容分类，让你随时发现和享受新鲜有趣的短视频！

![DEMO](docs/DEMO.mp4)

## 功能亮点

- **视频播放**：支持播放、暂停、进度条拖拽，让你完全掌控观看节奏。
- **内容分类**：热门视频、体育频道等多种分类，轻松找到你感兴趣的内容。
- **视频切换**：键盘上下键即可切换视频，无缝浏览体验。
- **后端支持**：强大的用户和视频管理模块，以及搜索功能。

## 快速开始

想要在本地运行TasteVideo？按照以下步骤操作：

### 前提条件

确保你的系统已经安装了以下软件：

- Node.js
- pnpm
- Python 3.8+
- pipenv 或 virtualenv

### 克隆源代码

首先，克隆这个仓库到你的本地机器：

```bash
git clone https://github.com/SupremeTechWizard/TasteVideo.git
cd TasteVideo
```

### 前端设置

进入前端项目目录，安装依赖，并启动开发服务器：

```bash
cd frontend
pnpm install
pnpm run dev
```

这时候，你的前端应用应该已经运行了。

### 后端设置

进入后端项目目录，设置虚拟环境，并安装依赖：

```bash
cd ../backend
pipenv shell # 或者使用 virtualenv
pipenv install # 或者使用 pip install -r requirements.txt
```

启动FastAPI服务器：

```bash
uvicorn main:app --reload
```

默认情况下，后端API会在 `http://localhost:8000` 上运行。

### 数据库迁移

确保你已经创建了数据库，并在后端项目的配置文件中设置了正确的连接字符串。然后执行迁移：

```bash
# 这里的迁移命令取决于你使用的ORM工具
alembic upgrade head
```

### 访问应用

现在，你可以通过浏览器访问 `http://localhost:8080` 来享受TasteVideo带来的精彩短视频了！
