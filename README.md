# Natural Language-Guided Drone Control with Reinforcement Learning

## 概要

本リポジトリは、3D物理シミュレーション環境ライブラリ [Genesis](https://genesis-embodied-ai.github.io/) を利用し、強化学習ライブラリ [rsl_rl](https://github.com/leggedrobotics/rsl_rl) のPPO（Proximal Policy Optimization）アルゴリズムを用いてドローン制御を学習させたプロジェクトです。(hover_*.pyとquadcopter_controller.pyはGenesisの配布コードを本タスクように書き換えたもの。)

特筆すべき点として、本プロジェクトでは**自然言語による指示をもとにドローンの行動方針を切り替える仕組み**を導入しています。これにより、単に目標に向かって直進するのではなく、障害物を回避したり、上下運動を組み合わせたりといった柔軟な行動が可能となります。

---

## 特徴

- **Genesisベースの物理シミュレーション環境**
  - ドローンや障害物を自由に配置できる3D空間を構築。
- **rsl_rlによるPPOアルゴリズムの導入**
  - 安定かつ高速な強化学習実装で学習を効率化。
- **自然言語による動作制御**
  - 簡単な指示文（例：「上昇しながら前に進め」）に対して、対応する報酬関数を切り替え。
  - 直進タスクでは解決できないような環境（障害物付き）に対応。
  - 現時点では環境からサンプリングされた自然言語指示を使用。将来的にはGUIからの入力に対応予定。

---

## 使用環境

- Ubuntu: 24.04.2 LTS
- Python: 3.10.5

---
