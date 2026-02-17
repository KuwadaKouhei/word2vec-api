#!/usr/bin/env python3
"""
chiVeモデルダウンロードスクリプト

利用可能なモデル:
  - v1.3-mc5   : 語彙数 2,530,791 / gensim 2.9GB  （最大・最高精度）
  - v1.3-mc15  : 語彙数 1,186,019 / gensim 1.3GB
  - v1.3-mc30  : 語彙数   759,011 / gensim 0.8GB
  - v1.3-mc90  : 語彙数   410,533 / gensim 0.5GB  （最小・高速）★推奨

mc = minimum count（最低出現頻度）。
数値が大きいほど語彙が少なく軽量だが、珍しい単語が含まれない。
"""

import argparse
import os
import tarfile
import urllib.request
import sys

BASE_URL = "https://sudachi.s3-ap-northeast-1.amazonaws.com/chive"

MODELS = {
    "v1.3-mc5": f"{BASE_URL}/chive-1.3-mc5_gensim.tar.gz",
    "v1.3-mc15": f"{BASE_URL}/chive-1.3-mc15_gensim.tar.gz",
    "v1.3-mc30": f"{BASE_URL}/chive-1.3-mc30_gensim.tar.gz",
    "v1.3-mc90": f"{BASE_URL}/chive-1.3-mc90_gensim.tar.gz",
    # v1.2系（参考）
    "v1.2-mc5": f"{BASE_URL}/chive-1.2-mc5_gensim.tar.gz",
    "v1.2-mc15": f"{BASE_URL}/chive-1.2-mc15_gensim.tar.gz",
    "v1.2-mc30": f"{BASE_URL}/chive-1.2-mc30_gensim.tar.gz",
    "v1.2-mc90": f"{BASE_URL}/chive-1.2-mc90_gensim.tar.gz",
}


def download_with_progress(url: str, dest: str):
    """プログレスバー付きダウンロード"""
    print(f"ダウンロード中: {url}")

    def reporthook(block_num, block_size, total_size):
        downloaded = block_num * block_size
        if total_size > 0:
            percent = min(100, downloaded * 100 / total_size)
            mb_downloaded = downloaded / (1024 * 1024)
            mb_total = total_size / (1024 * 1024)
            sys.stdout.write(
                f"\r  [{percent:5.1f}%] {mb_downloaded:.1f}MB / {mb_total:.1f}MB"
            )
        else:
            mb_downloaded = downloaded / (1024 * 1024)
            sys.stdout.write(f"\r  {mb_downloaded:.1f}MB downloaded")
        sys.stdout.flush()

    urllib.request.urlretrieve(url, dest, reporthook)
    print("\n  ダウンロード完了!")


def extract_tar_gz(filepath: str, dest_dir: str):
    """tar.gzを解凍"""
    print(f"解凍中: {filepath}")
    with tarfile.open(filepath, "r:gz") as tar:
        tar.extractall(path=dest_dir)
    print("  解凍完了!")


def main():
    parser = argparse.ArgumentParser(description="chiVeモデルダウンロード")
    parser.add_argument(
        "--model",
        default="v1.3-mc90",
        choices=list(MODELS.keys()),
        help="ダウンロードするモデル（デフォルト: v1.3-mc90）",
    )
    parser.add_argument(
        "--output-dir",
        default="models",
        help="保存先ディレクトリ（デフォルト: models/）",
    )
    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    url = MODELS[args.model]
    tar_filename = url.split("/")[-1]
    tar_path = os.path.join(args.output_dir, tar_filename)

    # ダウンロード
    if os.path.exists(tar_path):
        print(f"既にダウンロード済み: {tar_path}")
    else:
        download_with_progress(url, tar_path)

    # 解凍
    extract_tar_gz(tar_path, args.output_dir)

    # 解凍後のファイル確認
    print(f"\n=== models/ ディレクトリの内容 ===")
    for root, dirs, files in os.walk(args.output_dir):
        for f in files:
            filepath = os.path.join(root, f)
            size_mb = os.path.getsize(filepath) / (1024 * 1024)
            print(f"  {filepath} ({size_mb:.1f}MB)")

    # .kvファイルのパスを表示
    model_name = args.model.replace("v", "chive-").replace("-", "-", 1)
    print(f"\n✅ 環境変数の設定例:")
    print(f'   export CHIVE_MODEL_PATH="models/{model_name}.kv"')
    print(f"\n   ※ 解凍後のディレクトリ構造に合わせてパスを調整してください")


if __name__ == "__main__":
    main()
