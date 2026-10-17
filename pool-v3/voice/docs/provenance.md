# 来源与缺口

仓库 https://github.com/PaulWoitaschek/Voice；8.9.0 commit aa413505e8b871255fb40a518d3ad2554cb69f9d；许可证 LICENSE.md。实际构建 voice-build-03，GitHub flavor，禁用专有库。voice-main-inspection 不是本题来源。

已读 README.md、docs/index.md、docs/about.md、docs/organizing.md、docs/faq.md。组织手册明确三种目录分组；FAQ说明平台媒体格式、睡眠暂停后的恢复及 Android Auto 的Play限制。源码含 features/bookmark 和 features/sleepTimer；文件存在不证明设备行为。

状态 DRAFT。尚无本机完整播放、音频采集、书签/变速/焦点证据、时间容差、完整设计图和题目验收。不得沿用早期自制小播放器的通过记录来证明本题可解。Golden、错误实现、多模型和独立人工复核均未完成。

局部设备 evidence：voice-explore-16 记录五个音频导入后的三本书；voice-library-check-01 核对书籍身份并打开 Field Journal；voice-chapter-selection-01 核对 Arrival/Return 并选择 Return；voice-restart-state-check-01 观察重开后保留章节选择。三张已检查的截图现列入 input/design，操作卡 AB-L01 至 AB-L06 明确各自证据边界。重启观察经过 AOT 编译和启动超时后的独立检查，不证明干净启动稳定性；模拟器仍为 -no-audio，未验证真实播放。详细过程见维护侧 references/voice-exploration.md。

input/audio-v01新增5段原创机器旁白，使用已有本机FFmpeg/libflite离线合成；2本各2章加根目录单文件书，跨书章节同名而内容不同。实际逐文件完整解码，约31至34秒，均非静音，含媒体元数据、SHA256、生成命令与工具快照。媒体生成成功不证明Voice播放成功。详细输入说明见 ../input/README.md（相对于题包根目录为 input/README.md）。
