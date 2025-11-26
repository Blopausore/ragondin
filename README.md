# Ragondin

Ragondin is a RAG create for personal use.


## Tutorial : First project

### Create and Connect

Here you create a project named **PROJECT_NAME** and connect it.

```sh
ragondin create [PROJECT_NAME]
```

```sh
ragondin connect [PROJECT_NAME]
```

### Add sources and Analyse it

Then you have to add sources for you project.

```sh
ragondin add [DIR_PATH]
```

You can check what sources have been added with

```sh
ragondin list
```

Then finally you can process it.

```sh
ragondin process
```

It will :
* Vectorize your documents
* Create the necessary indexes




Then 
```sh
ragondin ask [PUT_QUESTION]
```



