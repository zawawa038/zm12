'''
if csv:
            try:
                # isPartial列を除外するかどうか
                if complete_data_only:
                    complete_data = data.drop(row=)
                elif exclude_partial and 'isPartial' in data.columns:
                    clean_data = data.drop(columns=['isPartial'])
                    clean_data.to_csv(csv, encoding='utf-8-sig')
                    typer.echo(f"\nデータを '{csv}' に保存しました（isPartial列を除外）。")
                else:
                    data.to_csv(csv, encoding='utf-8-sig')
                    typer.echo(f"\nデータを '{csv}' に保存しました。")
            except Exception as e:
                typer.echo(f"CSV保存エラー: {e}", err=True)
'''

'''
if csv:
            try:
                from datetime import datetime
                
                # ベースフォルダの作成
                base_folder = Path(csv_folder)
                
                # 日付別フォルダオプション
                if date_folder:
                    today = datetime.now().strftime("%Y-%m-%d")
                    folder_path = base_folder / today
                else:
                    folder_path = base_folder
                
                # フォルダ作成
                folder_path.mkdir(parents=True, exist_ok=True)
                
                # フルパスの作成
                csv_path = folder_path / csv
            #try:
                #save_data = data.copy()  # 元データを保持
                #excluded_rows = 0
                
                # 部分的データ（行）の除外
                if completed_only and 'isPartial' in save_data.columns:
                    original_count = len(save_data)
                    save_data = save_data[save_data['isPartial'] == False]
                    excluded_rows = original_count - len(save_data)
                
                # isPartial列の除外
                if (exclude_partial or completed_only) and 'isPartial' in save_data.columns:
                    save_data = save_data.drop(columns=['isPartial'])
                
                # 保存
                save_data.to_csv(csv, encoding='utf-8-sig')
                
                # 保存結果の表示
                message = f"\nデータを '{csv}' に保存しました"
                if excluded_rows > 0:
                    message += f"（{excluded_rows}件の部分的データを除外）"
                if exclude_partial or completed_only:
                    message += "（isPartial列を除外）"
                message += "。"
                
                typer.echo(message)
                
            except Exception as e:
                typer.echo(f"CSV保存エラー: {e}", err=True)
                '''