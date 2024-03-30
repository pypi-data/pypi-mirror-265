

        pad_width = window_len // 2 + 1
        if pad_mode is not None:
            series_index = np.concatenate(
                (
                    pd.date_range(
                        end=ttsd.index[0] - tdelt,
                        periods=pad_width,
                        freq=ttsd.index.freq,
                    ),
                    ttsd.index,
                    pd.date_range(
                        start=ttsd.index[-1] + tdelt,
                        periods=pad_width,
                        freq=ttsd.index.freq,
                    ),
                ),
                axis=None,
            )
            ttsd = pd.DataFrame(index=series_index)
            for col in tsd.columns:
                ttsd[col] = np.pad(tsd[col].values, pad_width, mode=pad_mode)
