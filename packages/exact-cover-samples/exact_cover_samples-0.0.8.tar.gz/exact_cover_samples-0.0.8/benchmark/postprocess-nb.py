# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: all,-hidden,-heading_collapsed,-run_control,-trusted
#     formats: py:percent
#     notebook_metadata_filter: all, -jupytext.text_representation.jupytext_version,
#       -jupytext.text_representation.format_version,-language_info.version, -language_info.codemirror_mode.version,
#       -language_info.codemirror_mode,-language_info.file_extension, -language_info.mimetype,
#       -toc, -rise, -version
#     text_representation:
#       extension: .py
#       format_name: percent
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
#   language_info:
#     name: python
#     nbconvert_exporter: python
#     pygments_lexer: ipython3
# ---

# %%
import pandas as pd
import matplotlib.pyplot as plt

# %%
# %matplotlib ipympl

# %% [markdown]
# # drawing benchmark results

# %% [markdown]
# ## loading results

# %%
df = pd.read_csv("results.csv", keep_default_na=False)
df.shape

# %%
df['lib-version'] = df['library'] + '-' + df['version']

# %%
df.head()

# %% [markdown]
# ## errors
#
# set time=nan on suspicious results, in case the benchmarking code has not

# %%
import math

df.loc[(df.computed == -1) | (df.error != ""), 'time'] = math.nan

df[(df.computed == -1) | (df.error != "")]


# %% [markdown]
# ## keeping only run 1 (if available)

# %%
run0 = df[df.run == 0]
run1 = df[df.run == 1]
if len(run1):
    df = run1
else:
    df = run0
df.shape

# %%
df.head()

# %% [markdown]
# ## drawing

# %% [markdown]
# ### keep only relevant columns

# %%
# only these columns
keep = "lib-version+problem+requested+time".split("+")

# %% [markdown]
# ### pivot

# %%
# pivot 
table = df[keep].pivot_table(columns=["requested", "lib-version"], index="problem", values="time")
table.head(5)

# %% [markdown]
# ### sort

# %%
# spot first column done by 'xcover'
for col in table.columns:
    size, algo = col
    if algo.startswith('xcover'):
        table.sort_values(by=col, inplace=True)
        break

table

# %% [markdown]
# ### draw - all solutions only

# %%
# requested=0 means all solutions
df_all_sizes = table.loc[:, 0]


df_all_sizes.plot(xticks=(range(len(df_all_sizes.index))))
plt.xticks(rotation=45, ha='right')
plt.subplots_adjust(bottom=0.3)

plt.savefig("benchmark.svg", format="svg")
plt.savefig("benchmark.png", format="png")
